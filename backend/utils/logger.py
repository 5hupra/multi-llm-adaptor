import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logger = logging.getLogger("adaptorLogs")
    logger.setLevel(logging.INFO)

    # prevent duplicates
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        "adaptorLogs.log", maxBytes=2_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger