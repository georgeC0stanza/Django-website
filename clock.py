from apscheduler.schedulers.blocking import BlockingScheduler

from rq import Queue
from worker import conn
from client_tracker import update_daemon


q = Queue(connection=conn)

sched = BlockingScheduler()
sched.configure(timezone="America/Denver")


@sched.scheduled_job("cron", day_of_week="sun", hour=0, minute="01")
def scheduled_job():
    print("Starting the update process")
    q.enqueue(update_daemon.start)


sched.start()
