import schedule
import time
def interval(every):
    print('Hi interval')
    def decorator(job_func):
        print('Hi decorator')
        from functools import wraps
        @wraps(job_func)
        def wrapper():
            print('Hi wrapper')
            return schedule.every(every).seconds.do(job_func)
        return wrapper
    return decorator


def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(2)