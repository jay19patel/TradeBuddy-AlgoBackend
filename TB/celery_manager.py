


# celery_app.py
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379/0')

# Configuration
app.conf.update(
    result_backend='redis://localhost:6379/0',
    timezone='Asia/Kolkata',
    enable_utc=True,
)

# Schedule the tasks
app.conf.beat_schedule = {
    'start-process': {
        'task': 'TB.base_execution.initialize_system',
        'schedule': crontab(minute=15, hour=9),  # 9:15 AM
    },
    'execute-every-15-minutes': {
        'task': 'TB.base_execution.execute_tradebuddy_abs',
        'schedule': crontab(minute='*/15', hour='9-15'),  # every 15 minutes from 9 AM to 3 PM
    },
    'end-process': {
        'task': 'TB.base_execution.shutdown_system',
        'schedule': crontab(minute=15, hour=15),  # 3:15 PM
    },
}
