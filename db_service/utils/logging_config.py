import json
import logging
from datetime import datetime
from functools import wraps

from utils.constants import SUCCESSFUL, FAILED


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "level": record.levelname,
            "module": record.module,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
            "filename": record.pathname,
        }
        return json.dumps(log_obj)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler for Fluentd (stdout)
console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())
logger.addHandler(console_handler)


def log_transfer_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_transfer_time = datetime.now()
        logger.info(f"{func.__name__}: Datatransfer started at {start_transfer_time}", stacklevel=2)
        try:
            func(*args, **kwargs)
            return_msg = SUCCESSFUL
        except Exception as e:
            return_msg = FAILED["message"]
        logger.info(f"{func.__name__}: Datatransfer finished: {datetime.now() - start_transfer_time}", stacklevel=2)

        return return_msg

    return wrapper


def exception_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {e}", stacklevel=2)

    return wrapper


def exception_handling_raise_e(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {e}", stacklevel=2)
            raise e

    return wrapper


def data_transfer_logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_transfer_time = datetime.now()
        try:
            logger.info(f"{func.__name__}: Query started at {start_transfer_time}", stacklevel=2)
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__}: Query finished: {datetime.now() - start_transfer_time}", stacklevel=2)
            return result
        except Exception as e:
            logger.error(f"Datatransfer failed. {func.__name__}: {e}", stacklevel=2)

    return wrapper
