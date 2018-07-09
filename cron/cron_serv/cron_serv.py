import signal
import time
from .scheduler import CronScheduler


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def init_scheduler(crontab_paths, logger):
    scheduler = CronScheduler()
    scheduler.read_crontabs(crontab_paths)
    cronjobs = scheduler.cronjob;
    logger.info("get {} cron job(s)".format(len(cronjobs)))
    scheduler_killer = GracefulKiller()
    scheduler.queue_in_jobs()
    logger.info("start scheduler")
    scheduler.start_scheduler()
    while True:
        if scheduler_killer.kill_now:
            scheduler.stop_scheduler()
            logger.info("stop scheduler")
            break
        else:
            time.sleep(0.5)
        pass
