# app/services/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.database import SessionLocal
import atexit
from datetime import datetime
from app.services.post_publisher import publish_post_by_id

scheduler = BackgroundScheduler()
# optional: persist jobs to DB via SQLAlchemyJobStore (requires DB URL)
jobstore = {"default": SQLAlchemyJobStore(url="sqlite:///./jobs.sqlite")}
# If you prefer Postgres, set `url` to your DATABASE_URL.
scheduler.configure(jobstores=jobstore)
scheduler.start()

# ensure scheduler shuts down cleanly
atexit.register(lambda: scheduler.shutdown(wait=False))

def schedule_post(post_id: int, run_at: datetime):
    """
    schedule a job to publish the post at run_at
    """
    job_id = f"publish_post_{post_id}"
    # remove existing job if present
    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass
    scheduler.add_job(lambda: publish_post_by_id(post_id), 'date', run_date=run_at, id=job_id)
    return job_id

def run_post_now(post_id: int):
    # run immediately in background
    scheduler.add_job(lambda: publish_post_by_id(post_id))
