from apscheduler.schedulers.background import BackgroundScheduler
from app.controllers.services_controller import auto_cancel_expired_borrowings, send_due_reminders
import logging
from flask import current_app

logging.basicConfig(level=logging.INFO)

def run_both_jobs():
    from app import create_app  
    app = create_app()
    
    with app.app_context():
        auto_cancel_expired_borrowings()
        send_due_reminders()

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # to test change hour='8,17', minute=0 to minute='*/1' for every 1 minutes
    if not scheduler.running:
        scheduler.add_job(run_both_jobs, 'cron',hour='8,17', minute=0)  # 8 AM and 5 PM
        
        scheduler.start()
        logging.info("Scheduler started.")
    else:
        logging.info("Scheduler is already running.")
    
    jobs = scheduler.get_jobs()
    for job in jobs:
        logging.info(f"Job {job.id} is scheduled to run next at {job.next_run_time}")


