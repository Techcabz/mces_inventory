def borrowing_auto_cancel_email(user_name, borrowing_id, end_date, custom_message=None):
    message = custom_message or "Your borrowing request has expired and was automatically cancelled."

    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #c0392b;">Borrowing Cancelled</h2>
                <p>Dear <strong>{user_name}</strong>,</p>
                <p>{message}</p>
                <p>Reference ID: <strong>{borrowing_id}</strong></p>
                <p>Expired on: <strong>{end_date.strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
                <p>If you still need the items, kindly submit a new request.</p>
                <br>
                <p style="margin-top: 30px;">Regards,<br><strong>MCES Inventory System</strong></p>
            </div>
        </body>
    </html>
    """
    
def borrowing_due_reminder_email(user_name, borrowing_id, end_date, custom_message=None):
    message = custom_message or "This is a friendly reminder that your borrowed items are due soon."

    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #2980b9;">Borrowing Due Reminder</h2>
                <p>Dear <strong>{user_name}</strong>,</p>
                <p>{message}</p>
                <p>Reference ID: <strong>{borrowing_id}</strong></p>
                <p>Due Date: <strong>{end_date.strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
                <p>Please make sure to return the borrowed items on or before the due date to avoid issues.</p>
                <br>
                <p style="margin-top: 30px;">Thank you,<br><strong>MCES Inventory System</strong></p>
            </div>
        </body>
    </html>
    """
