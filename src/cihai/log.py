"""Log utilities for cihai.

cihai.log
~~~~~~~~~

"""
import logging
import time
import typing as t

from colorama import Fore, Style, init

LEVEL_COLORS = {
    "DEBUG": Fore.BLUE,  # Blue
    "INFO": Fore.GREEN,  # Green
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.RED,
}


class LogFormatter(logging.Formatter):
    def __init__(self, color: bool = True, **kwargs: t.Any):
        init()
        logging.Formatter.__init__(self, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = f"Bad message ({e!r}): {record.__dict__!r}"

        date_format = "%H:%m:%S"
        record.asctime = time.strftime(date_format, self.converter(record.created))

        prefix = self.template(record) % record.__dict__

        formatted = prefix + " " + record.message
        return formatted.replace("\n", "\n    ")

    def template(self, record: logging.LogRecord) -> str:
        """Return the prefix for the log message. Template for Formatter.

        Parameters
        ----------
        record : :py:class:`logging.LogRecord`
            Passed in from inside the :py:meth:`logging.Formatter.format` record.
        """
        reset = [Style.RESET_ALL]
        levelname = [
            LEVEL_COLORS.get(record.levelname, ""),
            Style.BRIGHT,
            "(%(levelname)s)",
            Style.RESET_ALL,
            " ",
        ]
        asctime = [
            "[",
            Fore.BLACK,
            Style.DIM,
            Style.BRIGHT,
            "%(asctime)s",
            Fore.RESET,
            Style.RESET_ALL,
            "]",
        ]
        name = [
            " ",
            Fore.WHITE,
            Style.DIM,
            Style.BRIGHT,
            "%(name)s",
            Fore.RESET,
            Style.RESET_ALL,
            " ",
        ]

        tpl = "".join(reset + levelname + asctime + name + reset)

        return tpl


class DebugLogFormatter(LogFormatter):
    """Provides greater technical details than standard log Formatter."""

    def template(self, record: logging.LogRecord) -> str:
        """Return the prefix for the log message. Template for Formatter.

        Parameters
        ----------
        record : :py:class:`logging.LogRecord`
            Passed in from inside the :py:meth:`logging.Formatter.format` record.
        """
        reset = [Style.RESET_ALL]
        levelname = [
            LEVEL_COLORS.get(record.levelname, ""),
            Style.BRIGHT,
            "(%(levelname)1.1s)",
            Style.RESET_ALL,
            " ",
        ]
        asctime = [
            "[",
            Fore.BLACK,
            Style.DIM,
            Style.BRIGHT,
            "%(asctime)s",
            Fore.RESET,
            Style.RESET_ALL,
            "]",
        ]
        name = [
            " ",
            Fore.WHITE,
            Style.DIM,
            Style.BRIGHT,
            "%(name)s",
            Fore.RESET,
            Style.RESET_ALL,
            " ",
        ]
        module_funcname = [Fore.GREEN, Style.BRIGHT, "%(module)s.%(funcName)s()"]
        lineno = [
            Fore.BLACK,
            Style.DIM,
            Style.BRIGHT,
            ":",
            Style.RESET_ALL,
            Fore.CYAN,
            "%(lineno)d",
        ]

        tpl = "".join(
            reset + levelname + asctime + name + module_funcname + lineno + reset
        )

        return tpl
