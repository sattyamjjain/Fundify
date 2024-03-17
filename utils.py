import functools
import logging
import os
from logging.handlers import RotatingFileHandler

import pandas as pd

from config import STORE_CONFIG


def get_logger(level=logging.INFO, max_size=1048576, backup_count=3):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    file_handler = RotatingFileHandler(
        "audit.log", maxBytes=max_size, backupCount=backup_count
    )
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def hop(start, stop, step):
    for i in range(start, stop, step):
        yield i
    yield stop


def ensure_directory(directory_key):
    def decorator_ensure_directory(func):
        @functools.wraps(func)
        def wrapper_ensure_directory(*args, **kwargs):
            directory_path = STORE_CONFIG[directory_key]
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            return func(*args, **kwargs)

        return wrapper_ensure_directory

    return decorator_ensure_directory


def save_dataframe(df: pd.DataFrame, file_path: str, append: bool = False):
    if append:
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, mode="w", header=True, index=False)
