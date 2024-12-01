from functools import cached_property
import logging
from typing import Literal
from app.core.settings import get_settings
import structlog

settings = get_settings()


class LoggerMixin:
    """Mixin that provides a class level 'logger' property."""

    @cached_property
    def logger(self) -> structlog.stdlib.BoundLogger:
        logger: structlog.stdlib.BoundLogger = structlog.getLogger(type(self).__qualname__)
        return logger.bind(logger=type(self).__name__)


def get_logger(func_name: str) -> structlog.stdlib.BoundLogger:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger(func_name)
    return logger.bind(logger=func_name)


def setup_logging(*, loglevel: int, logformat: Literal["plain", "json"] = "plain"):
    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    if logformat not in {"plain", "json"}:
        logformat = "plain"

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.dev.ConsoleRenderer(exception_formatter=structlog.dev.plain_traceback),
                    ],
                    "foreign_pre_chain": pre_chain,
                },
                "json": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.processors.dict_tracebacks,
                        structlog.processors.JSONRenderer(),
                    ],
                    "foreign_pre_chain": pre_chain,
                },
            },
            "filters": {
                "error_and_above": {
                    "()": lambda: lambda record: record.levelno >= logging.ERROR,
                },
                "bellow_error": {
                    "()": lambda: lambda record: record.levelno < logging.ERROR,
                },
            },
            "handlers": {
                "stdout_output": {
                    "class": "logging.StreamHandler",
                    "filters": ["bellow_error"],
                    "formatter": logformat,
                    "level": loglevel,
                    "stream": "ext://sys.stdout",
                },
                "stderr_output": {
                    "class": "logging.StreamHandler",
                    "filters": ["error_and_above"],
                    "formatter": logformat,
                    "level": loglevel,
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {},
            "root": {
                "level": loglevel,
                "handlers": [
                    "stdout_output",
                    "stderr_output",
                ],
                "propagate": True,
            },
        }
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
