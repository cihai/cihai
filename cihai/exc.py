"""Exceptions raised from the Cihai library."""


class CihaiException(Exception):
    """Base Cihai Exception class."""


class ImportStringError(ImportError, CihaiException):
    """
    Provides information about a failed :func:`import_string` attempt.

    Notes
    -----
    This is from werkzeug.utils c769200 on May 23, LICENSE BSD.
    https://github.com/pallets/werkzeug

    Changes:
    - Deferred load import import_string from cihai.util
    - Format with black
    """

    #: String in dotted notation that failed to be imported.
    import_name = None
    #: Wrapped exception.
    exception = None

    def __init__(self, import_name, exception):
        from .utils import import_string

        self.import_name = import_name
        self.exception = exception

        msg = (
            'import_string() failed for %r. Possible reasons are:\n\n'
            '- missing __init__.py in a package;\n'
            '- package or module path not included in sys.path;\n'
            '- duplicated package or module name taking precedence in '
            'sys.path;\n'
            '- missing module, class, function or variable;\n\n'
            'Debugged import:\n\n%s\n\n'
            'Original exception:\n\n%s: %s'
        )

        name = ''
        tracked = []
        for part in import_name.replace(':', '.').split('.'):
            name += (name and '.') + part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, '__file__', None)))
            else:
                track = ['- %r found in %r.' % (n, i) for n, i in tracked]
                track.append('- %r not found.' % name)
                msg = msg % (
                    import_name,
                    '\n'.join(track),
                    exception.__class__.__name__,
                    str(exception),
                )
                break

        ImportError.__init__(self, msg)

    def __repr__(self):
        return '<%s(%r, %r)>' % (
            self.__class__.__name__,
            self.import_name,
            self.exception,
        )
