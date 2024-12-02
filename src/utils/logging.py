"""custom logger setting."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING
from typing import ClassVar

if TYPE_CHECKING:
    from pathlib import Path


class SetColor(logging.Formatter):
    """A custom logging formatter to colorize terminal output.

    Args:
        format(record: logging.LogRecord): Format the given log.
    """

    # Define color codes for terminal display
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    bold_light_red = "\x1b[91m;1m"
    reset = "\x1b[0m"

    # Format strings for logging output
    log_format = "%(asctime)s - %(name)s - %(levelname)s"
    log_format += "- %(message)s (%(filename)s:%(lineno)d)"

    # Create a dictionary to map log levels to colorized format strings
    FORMATS: ClassVar[dict] = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: grey + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
        logging.exception: bold_light_red + log_format + reset,
    }

    def __init__(self, *args: str, **kwargs: str) -> None:
        """Initialize the SetColor logging formatter."""
        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        """Format the given log.

        Args:
            record(logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message as a string.
        """
        # Get the log format for the given log level
        log_fmt = self.FORMATS.get(record.levelno)

        # Create a formatter with the given log format
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")

        return formatter.format(record)


class SetLogConfig(SetColor):
    """A SetLogConfig with customizable log settings.

    Args:
        log_level(int): Default log level is INFO.
        log_file(str): Default log file name is "main.log".
        max_bytes(int): Default maximum log file size is 200 MB.
        backup_counts(int): Default backup count is 5.
    """

    def __init__(
        self,
        log_level: int = logging.INFO,
        log_file: str | None = "main.log",
        max_bytes: int = 200000000,
        backup_counts: int = 5,
    ) -> None:
        """Initialize the SetLogConfig object with customizable log settings."""
        # Initialize StreamHandler for terminal display
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(SetColor())

        # Configure log settings
        # Format for logging to file
        log_format = "%(asctime)s - %(name)s - %(levelname)s"
        # Add filename and line number
        log_format += "- %(message)s (%(filename)s:%(lineno)d)"
        # Set up logging to console stream
        logging.basicConfig(
            level=log_level,
            format=log_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[self.stream_handler],
        )
        # Set up logging to file
        if log_file != "None/None":
            log_file = log_file.replace("None/", "./")

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_counts,
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(logging.Formatter(log_format))
            logging.getLogger().addHandler(file_handler)

        # Get the logger instance
        self.logger = logging.getLogger()


class StreamToLogger:
    """A custom logging handler that writes log messages to a logger object.

    Args:
        logger(logging.Logger): An instance of logging.Logger to write log.
        log_level(int): The minimum log level for messages to be logged.

    """

    def __init__(
        self, logger: logging.Logger, log_level: int = logging.ERROR
    ) -> None:
        """Initialize the StreamToLogger."""
        self.logger = logger
        self.log_level = log_level
        self.linebuf: list[str] = []

    def write(self, buf: str) -> None:
        """Write log messages to the logger object.

        Args:
            buf(str): The target log message to write in the logger.
        """
        for line in buf.rstrip().splitlines():
            # If a line contains only a single whitespace character,
            # it is assumed to be an empty line
            # and is appended to the line buffer.
            if len(line) == 1:
                self.linebuf.append(line)
            else:
                # When the line contains log message,
                # combine the lines in the buffer and the new line
                # and log it with the provided logger and log level.
                msg = "".join([*self.linebuf, line.rstrip()])
                self.logger.log(self.log_level, msg)
                # After logging,
                # clear the line buffer for the next log message.
                self.linebuf = []

    def flush(self) -> None:
        """Flush."""


class SetLogger:
    """A logging configuration class that initializes and sets up a logger.

    Args:
        log_path(str|Path|None): The path to the log directory.
                                If None, only the terminal display.
        log_file_name(str|Path|None): The name of the log file.
                                    If None, only the terminal display.
        log_level(int) : The level of the log. Default is logging.INFO.
    """

    def __init__(
        self,
        log_path: str | Path | None = None,
        log_name: str | Path | None = None,
        log_level: int = logging.INFO,
    ) -> None:
        self.log_path = log_path
        self.log_name = log_name
        self.log_level = log_level
        self.log_file = f"{self.log_path!s}/{self.log_name!s}"
        self.log_config = SetLogConfig(
            log_file=self.log_file, log_level=self.log_level
        )
        self.logger = self.log_config.logger
        sys.stderr = StreamToLogger(self.logger)
