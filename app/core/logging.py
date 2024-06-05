import logging
from functools import lru_cache

from rich.logging import RichHandler
from pydantic import BaseModel

DATE_FORMAT = "%d-%b-%y %H:%M:%S"
LOGGER_FORMAT = "%(levelname)s: %(asctime)s \t%(message)s"
LOGGER_HANDLER = None


class LoggerConfig(BaseModel):
    handlers: list
    format: str
    date_format: str
    level: str = logging.DEBUG


@lru_cache()
def get_logger_config() -> LoggerConfig:
    return LoggerConfig(
        handlers=[RichHandler(rich_tracebacks=True)],
        format=LOGGER_FORMAT,
        date_format=DATE_FORMAT,
    )


logger_config = get_logger_config()

logging.basicConfig(
    level=logger_config.level,
    format=logger_config.format,
    datefmt=logger_config.date_format,
    handlers=logger_config.handlers,
)
