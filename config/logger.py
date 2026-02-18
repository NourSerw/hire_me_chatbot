import logging
import os
from logging.handlers import RotatingFileHandler

# ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def setup_logger(name: str = "app_logger"):
    logger = logging.getLogger(name)

    # prevent adding handlers multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # terminal output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # rotating file output
    file_handler = RotatingFileHandler(
        "logs/logs.log",
        maxBytes=5_000_000,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger