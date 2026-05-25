import schedule
import time
from datetime import datetime
import threading
from engine import run_predictions

def run_daily_predictions():
    """Run predictions and send to Telegram/Discord"""
    print(f"[{datetime.now()}] Running scheduled daily predictions...")
    run_predictions(send_to_telegram=True, send_to_discord=True)

def start_scheduler():
    """Start background scheduler for daily predictions"""
    schedule.every().day.at("08:00").do(run_daily_predictions)  # 8 AM daily
    
    print("⏰ Scheduler started! Daily predictions at 08:00 AM")
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    # Run in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
