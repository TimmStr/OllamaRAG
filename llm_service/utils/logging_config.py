import json
import logging
from datetime import datetime
from functools import wraps


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'level': record.levelname,
            'module': record.module,
            'lineno': record.lineno,
            'funcName': record.funcName,
            'message': record.getMessage(),
            'timestamp': self.formatTime(record, self.datefmt),
            'filename': record.pathname,
        }
        return json.dumps(log_obj)


# Logging-Config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler for Fluentd (stdout)
console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())

logger.addHandler(console_handler)


def log_report_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_transfer_time = datetime.now()

        s = " " + (", ".join(map(lambda x: f"{x[0]}:{x[1]}", kwargs.items())))
        logger.info(f"{func.__name__}: Request started at {start_transfer_time}{s}", stacklevel=2)

        result = func(*args, **kwargs)

        logger.info(f"{func.__name__}: Request ended successfully at {datetime.now() - start_transfer_time}{s}",
                    stacklevel=2)

        return result

    return wrapper


def log_llm_report_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_transfer_time = datetime.now()
        s = " " + (", ".join(map(lambda x: f"{x[0]}:{x[1]}", kwargs.items())))
        logger.info(f"{func.__name__}: LLM Request started at {start_transfer_time}{s}", stacklevel=2)

        result = func(*args, **kwargs)

        logger.info(
            f"{func.__name__}: LLM Request ended successfully at {datetime.now() - start_transfer_time}{s}",
            stacklevel=2)

        return result

    return wrapper


def exception_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {e}", exc_info=True, stacklevel=2)

    return wrapper


def exception_handling_raise_e(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {e}", exc_info=True, stacklevel=2)
            raise e

    return wrapper
