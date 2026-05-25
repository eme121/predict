from engine import run_predictions
from scheduler import start_scheduler

def start_all():
    """Start scheduler + predictions"""
    start_scheduler()
    run_predictions()

if __name__ == "__main__":
    start_all()
