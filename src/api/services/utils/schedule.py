import schedule
import signal
import sys
import time
def interval(every):
    def decorator(job_func):
        def wrapper(instance, *args, **kwargs):
            return schedule.every(every).seconds.do(job_func, instance)
        return wrapper
    return decorator

def signal_handler(sig, frame):
    print('\nClearing scheduled jobs')
    schedule.clear()
    sys.exit(0)

def run_scheduled_jobs():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        schedule.run_pending()
        time.sleep(2)