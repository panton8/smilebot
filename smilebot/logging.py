import logging

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=level.upper(), format=LOG_FORMAT)
    # Third-party noise: aiogram logs every update at INFO level.
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
