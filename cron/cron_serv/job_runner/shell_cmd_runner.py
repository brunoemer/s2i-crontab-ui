import subprocess
import sys
import time
import traceback
from ..logger import ConsoleLogger


def gen_run_sh_job(command, logger=ConsoleLogger('cron_serv.local-runner')):
    """
    Create APScheduler compatible job function for it to schedule to run.
    :param logger: logger for job runner
    :param command: the shell command to execute
    :return: parameter less function
    """

    def run_sh(command=command,logger=logger):
        logger.info("run scheduled job {0} at: {1}".format(command, time.strftime("%Y/%m/%d %H:%M:%S")))
        # noinspection PyBroadException
        try:
            assert sys.version_info >= (2, 7)
            if sys.version_info >= (3, 5):
                complete_process = subprocess.run(args=[command], universal_newlines=True, stdout=subprocess.PIPE, shell=True)
                if complete_process.stderr and len(complete_process.stderr.splitlines()) > 0:
                    logger.info(complete_process.stderr.splitlines())
                pass
            else:
                out = subprocess.check_output(args=[command], universal_newlines=True, shell=True)
                if out and len(out) > 0:
                    logger.info(out)
                pass
        except subprocess.CalledProcessError as e:
            logger.error("Run sh job failed:\n%s", e.output)
            if sys.version_info >= (3, 5):
                logger.error("stdout=\n%s", e.stdout)
                logger.error("stderr=\n%s", e.stderr)
                pass
        except:
            logger.error("Run sh job failed with some other error!\n%s", traceback.format_exc())

    return run_sh
