from datetime import datetime
from celery_worker import shared_task
from app.services.services import CRUDService
from app.models.borrowing_models import Borrowing
from app.models.inventory_models import Inventory
from app.models.borrowing_details_model import BorrowingDetails
from app.extensions import mail
from flask_mail import Message
from app.utils.email_templates import borrowing_auto_cancel_email, borrowing_due_reminder_email
from config import Config

cancel_service = CRUDService(BorrowingDetails)
inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)

@shared_task
def auto_cancel_expired_borrowings_task():
    now = datetime.utcnow()
    expired_borrowings = borrowing_service.get(status='pending')

    cancelled_count = 0
    for borrowing in expired_borrowings:
        if borrowing.end_date and borrowing.end_date < now:
            user = borrowing.user
            if user and user.email:
                for cart_item in borrowing.cart_items:
                    inventory = inventory_service.get_one(id=cart_item.inventory_id)
                    if inventory:
                        inventory.quantity += cart_item.quantity
                        inventory.status = 'available' if inventory.quantity > 0 else inventory.status
                        inventory_service.update(inventory)

                borrowing_service.update(borrowing.id, status="cancelled")
                cancel_service.create(borrowing_id=borrowing.id, cancel_reason="Auto-cancelled due to expiration")
                cancelled_count += 1

                html_body = borrowing_auto_cancel_email(
                    user_name=user.fullname.title(),
                    borrowing_id=borrowing.reference_number,
                    end_date=borrowing.end_date,
                    custom_message="This is an automated notice that your borrowing request has expired and was automatically cancelled."
                )

                msg = Message(
                    sender=('MCES Inventory System - Auto Cancel', Config.MAIL_DEFAULT_SENDER),
                    subject='Your Borrowing Request Has Been Cancelled',
                    recipients=[user.email],
                    html=html_body
                )
                mail.send(msg)

    return f'Auto-cancelled {cancelled_count} expired borrowings.'


@shared_task
def send_due_reminders_task():
    now = datetime.utcnow()
    approved_borrowings = borrowing_service.get(status='approved')

    reminded_count = 0
    for borrowing in approved_borrowings:
        if borrowing.end_date:
            days_until_due = (borrowing.end_date - now).days
            if days_until_due <= 1:
                user = borrowing.user
                if user and user.email:
                    html_body = borrowing_due_reminder_email(
                        user_name=user.fullname.title(),
                        borrowing_id=borrowing.reference_number,
                        end_date=borrowing.end_date,
                        custom_message=(
                            "Reminder: Your borrowed items are due soon." if days_until_due == 1
                            else "Reminder: Your borrowed items are now due."
                        )
                    )

                    msg = Message(
                        sender=('MCES Inventory System - Reminder', Config.MAIL_DEFAULT_SENDER),
                        subject='Borrowing Due Reminder',
                        recipients=[user.email],
                        html=html_body
                    )
                    mail.send(msg)
                    reminded_count += 1

    return f'Sent {reminded_count} due reminders.'


