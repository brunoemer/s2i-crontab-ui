from tzlocal import get_localzone
from apscheduler.schedulers.background import BackgroundScheduler as BG_scheduler
from .parse_crontab import parse_crontabs
from .job_runner.shell_cmd_runner import gen_run_sh_job


class CronScheduler:
    """
    APScheduler wrapper
    """
    tz = get_localzone()
    scheduler = BG_scheduler(timezone=tz)
    __cron_entries = list()

    def read_crontabs(self, file_paths):
        self.__cron_entries = parse_crontabs(file_paths)

    def queue_in_jobs(self):
        for job in self.__cron_entries:
            self.scheduler.add_job(gen_run_sh_job(job.command), 'cron',
                                   day_of_week=job.day_of_week,
                                   month=job.month,
                                   day=job.day,
                                   hour=job.hour,
                                   minute=job.minute,
                                   name=job.command)

    def start_scheduler(self):
        self.scheduler.start()

    def stop_scheduler(self):
        self.scheduler.shutdown()

    @property
    def cronjob(self):
        return self.__cron_entries
