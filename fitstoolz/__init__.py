import logging
from importlib import metadata

__version__ = metadata.version(__package__)


def set_logger(name, level="INFO"):
    if isinstance(level, str):
        level = getattr(logging, level, 10)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)-8s| %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
