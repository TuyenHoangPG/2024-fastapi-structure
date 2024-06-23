import datetime
import json
import logging
import sys
from pathlib import Path

from asgi_correlation_id.context import correlation_id
from loguru import logger

from ..constants.constant import loglevel_mapping


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls, config_path: Path):
        config = cls.load_logging_config(config_path)
        logging_config = config.get("logger")
        log_filename = datetime.datetime.now().strftime("app_%Y-%m-%d.log")

        logger = cls.customize_logging(
            Path(__file__).resolve().parents[3] / "logs" / log_filename,
            level=logging_config.get("level"),
            retention=logging_config.get("retention"),
            rotation=logging_config.get("rotation"),
            format=logging_config.get("format"),
        )
        return logger

    @classmethod
    def customize_logging(
        cls,
        filepath: Path,
        level: str,
        rotation: str,
        retention: str,
        format: str,
    ):
        def correlation_id_filter(record):
            record["correlation_id"] = correlation_id.get()
            return record["correlation_id"]

        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            filter=correlation_id_filter,
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            filter=correlation_id_filter,
        )

        logging.getLogger("passlib").setLevel(logging.ERROR)
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=0,
        )
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id="app", method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
