import logging
from os.path import join, isfile, getctime
from os import listdir, remove
from datetime import date, timedelta
from logging import handlers
from .vars import variables


logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logFilePath = "./logs/API Server.log"
file_handler = handlers.TimedRotatingFileHandler(
    filename=logFilePath,
    when='midnight',
    interval=1,
    backupCount=int(variables.LOG_AGE))
file_handler.suffix = "%Y%m%d"
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def log_cleaner(fold: str = "./logs"):
    """
    Cleans old log files based on threshold set.
    If logs are in a different folder you can feed in the path
    """
    files = [join(fold, f) for f in listdir(fold) if isfile(join(fold, f))]

    for file in files:
        try:
            if file.endswith(".log"):
                pass
            else:
                file_date = date.fromtimestamp(getctime(file))
                threshold_date = date.today() - timedelta(days=int(variables.LOG_AGE))
                if file_date < threshold_date:
                    remove(file)
        except Exception as del_err:
            logger.error(str(del_err))
