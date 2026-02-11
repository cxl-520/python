from __future__ import annotations

import logging
from logging import handlers
from pathlib import Path

try:
    from colorama import Fore, Style, init as colorama_init
except Exception:  # pragma: no cover - optional dependency
    Fore = None
    Style = None
    colorama_init = None


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN if Fore else "",
        logging.INFO: Fore.GREEN if Fore else "",
        logging.WARNING: Fore.YELLOW if Fore else "",
        logging.ERROR: Fore.RED if Fore else "",
        logging.CRITICAL: Fore.MAGENTA if Fore else "",
    }

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL if Style else ""
        return f"{color}{message}{reset}"


DEFAULT_LOGGER_NAME = "app"


def setup_logging(
    log_dir: str | Path = "logs",
    log_file: str = "app.log",
    level: int = logging.INFO,
    report_file: str | None = None,
    report_level: int = logging.INFO,
) -> None:
    log_path = Path(log_dir).resolve()
    log_path.mkdir(parents=True, exist_ok=True)
    log_file_path = log_path / log_file

    if colorama_init:
        colorama_init()

    logger = logging.getLogger(DEFAULT_LOGGER_NAME)
    logger.setLevel(level)
    logger.handlers = []
    logger.propagate = False

    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    file_handler = handlers.RotatingFileHandler(
        log_file_path, maxBytes=1_048_576, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(fmt, datefmt))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(ColorFormatter(fmt, datefmt))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if report_file:
        report_path = log_path / report_file
        report_handler = handlers.RotatingFileHandler(
            report_path, maxBytes=2_097_152, backupCount=3, encoding="utf-8"
        )
        report_handler.setLevel(report_level)
        report_handler.setFormatter(logging.Formatter(fmt, datefmt))
        logger.addHandler(report_handler)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or DEFAULT_LOGGER_NAME)


def debug(msg: str, *args, **kwargs) -> None:
    get_logger().debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
    get_logger().info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
    get_logger().warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
    get_logger().error(msg, *args, **kwargs)


def critical(msg: str, *args, **kwargs) -> None:
    get_logger().critical(msg, *args, **kwargs)
