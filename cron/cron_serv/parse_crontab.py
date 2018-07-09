from crontab import CronTab
import re


def parse_crontab(file_path):
    file_cron = CronTab(tabfile=file_path)
    jobs = list()
    for entry in [job for job in file_cron if job.is_enabled()]:
        cron_entry = CronEntry(command=str(entry.command),
                               minute=str(entry.minute),
                               hour=str(entry.hour),
                               day=str(entry.day),
                               month=str(entry.month),
                               day_of_week=str(entry.dow),
                               comment=str(entry.comment))
        jobs.append(cron_entry)
        pass
    return jobs


def parse_crontabs(file_paths):
    ret = list()
    for file_path in file_paths:
        ret.extend(parse_crontab(file_path))
        pass
    return ret


class CronEntry:
    """
    Custom structure for store parsed crontab entry.
    """
    _pattern = '@"(?P<runner>[\w ]+)"\s*:\s*(?P<comment>.*)$'
    _remote_info = re.compile(_pattern)
    _comment = None
    _local_run = True
    _runner_name = 'localhost'

    def __init__(self, command=None, minute=None, hour=None, day=None, month=None, day_of_week=None, comment=None):
        self._command = command
        self._minute = minute
        self._hour = hour
        self._day = day
        self._month = month
        self._day_of_week = day_of_week
        self._parse_comment(comment)

    def _parse_comment(self, comment):
        result = self._remote_info.match(comment)
        if result:
            self._local_run = False
            self._runner_name = result.group('runner')
            self._comment = result.group('comment')
        else:
            self._comment = comment

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value):
        self._minute = value

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        self._hour = value

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        self._day = value

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        self._month = value

    @property
    def day_of_week(self):
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, value):
        self._day_of_week = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    @property
    def is_local(self):
        return self._local_run

    @property
    def runner(self):
        return self._runner_name
