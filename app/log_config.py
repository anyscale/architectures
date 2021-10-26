import logging
import os
import sys

from loguru import logger

LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING").upper()
JSON_LOGS = True if os.environ.get("JSON_LOGS", "1") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_level=LOG_LEVEL):
    # intercept everything at the root logger
    level = logging.getLevelName(log_level.upper())
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(level)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])
