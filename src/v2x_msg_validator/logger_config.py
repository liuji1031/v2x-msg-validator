import logging
import os

LOG_LVL = os.getenv("VALIDATOR_LOG_LEVEL", "INFO")

LOG_LVL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

logging.basicConfig(
    level=LOG_LVL_MAP.get(LOG_LVL, logging.INFO),
    format="[%(asctime)s - %(name)s:line[%(lineno)d] - %(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
