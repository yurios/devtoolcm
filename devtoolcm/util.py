import inspect
import logging


def init_logging(level: int = logging.INFO, include_logger_name: bool = False):
    stdout_handler = logging.StreamHandler()
    stdout_handler.level = level
    log_format = '[%(levelname)s]'
    if include_logger_name:
        log_format += ' [%(name)s]'
    log_format += ' > %(message)s'
    stdout_handler.setFormatter(logging.Formatter(log_format))
    logging.basicConfig(level=logging.INFO, handlers=[stdout_handler])


def get_logger(stak_index: int = 1):
    frm = inspect.stack()[stak_index]
    mod = inspect.getmodule(frm[0])
    return logging.getLogger(mod.__name__)
