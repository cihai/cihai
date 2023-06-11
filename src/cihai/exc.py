"""Exceptions raised from the Cihai library."""
import typing as t


class CihaiException(Exception):
    """Base Cihai Exception class."""


class ImportStringError(ImportError, CihaiException):
    """
    Provides information about a failed :func:`import_string` attempt.

    Notes
    -----
    This is from werkzeug.utils d36aaf1 on August 20 2022, LICENSE BSD.
    https://github.com/pallets/werkzeug

    Changes:
    - Deferred load import import_string from cihai.util
    - Format with black
    """

    #: String in dotted notation that failed to be imported.
    import_name: str
    #: Wrapped exception.
    exception: BaseException

    def __init__(
        self, import_name: str, exception: t.Union[ModuleNotFoundError, ImportError]
    ) -> None:
        from .utils import import_string

        self.import_name = import_name
        self.exception = exception
        msg = import_name
        name = ""
        tracked = []
        for part in import_name.replace(":", ".").split("."):
            name = f"{name}.{part}" if name else part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, "__file__", None)))
            else:
                track = [f"- {n!r} found in {i!r}." for n, i in tracked]
                track.append(f"- {name!r} not found.")
                track_str = "\n".join(track)
                msg = (
                    f"import_string() failed for {import_name!r}. Possible reasons"
                    f" are:\n\n"
                    "- missing __init__.py in a package;\n"
                    "- package or module path not included in sys.path;\n"
                    "- duplicated package or module name taking precedence in"
                    " sys.path;\n"
                    "- missing module, class, function or variable;\n\n"
                    f"Debugged import:\n\n{track_str}\n\n"
                    f"Original exception:\n\n{type(exception).__name__}: {exception}"
                )
                break

        super().__init__(msg)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}({self.import_name!r}, {self.exception!r})>"
