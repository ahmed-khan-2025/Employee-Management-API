import logging
import os

from logging.handlers import RotatingFileHandler


def setup_logging():

    os.makedirs(
        "logs",
        exist_ok=True
    )

    logger = logging.getLogger(
        "employee_management"
    )

    logger.setLevel(
        logging.INFO
    )

    if logger.handlers:

        return logger

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )

    return logger