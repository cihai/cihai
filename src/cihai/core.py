"""Cihai core functionality."""
import inspect
import logging
import pathlib
import typing as t

from cihai._internal.config_reader import ConfigReader
from cihai.data.unihan.dataset import Unihan
from unihan_etl.util import merge_dict

from . import exc, extend
from .config import expand_config
from .constants import DEFAULT_CONFIG, UNIHAN_CONFIG, app_dirs
from .db import Database
from .utils import import_string

if t.TYPE_CHECKING:
    from typing_extensions import TypeGuard

    from cihai.types import ConfigDict, UntypedDict

    DS = t.TypeVar("DS", bound=t.Type[extend.Dataset])


log = logging.getLogger(__name__)


class CihaiConfigError(exc.CihaiException):
    def __init__(self) -> None:
        return super().__init__("Invalid exception with configuration")


def is_valid_config(config: "UntypedDict") -> "TypeGuard[ConfigDict]":
    return True


class Cihai:
    """
    Central application object.

    By default, this automatically adds the UNIHAN dataset.

    Attributes
    ----------
    config : dict

    Notes
    -----
    Inspired by the early pypa/warehouse application object [1]_.

    **Configuration templates**

    The ``config`` :py:class:`dict` parameter supports a basic template system
    for replacing :term:`XDG Base Directory` directory variables, tildes
    and environmentas variables. This is done by passing the option dict
    through :func:`cihai.config.expand_config` during initialization.

    Examples
    --------
    To use cihai programmatically, invoke and install the UNIHAN [2]_ dataset:

    .. literalinclude:: ../examples/basic_usage.py
        :language: python

    Above: :attr:`~cihai.data.unihan.bootstrap.is_bootstrapped` can check if the system
    has the database installed.

    References
    ----------
    .. [1] PyPA Warehouse on GitHub. https://github.com/pypa/warehouse.
       Accessed sometime in 2013.
    .. [2] UNICODE HAN DATABASE (UNIHAN) documentation.
       https://www.unicode.org/reports/tr38/. Accessed March 31st, 2018.
    """

    #: :py:class:`dict` of default config, can be monkey-patched during tests
    default_config: "UntypedDict" = DEFAULT_CONFIG
    config: "ConfigDict"
    unihan: Unihan
    sql: Database

    def __init__(
        self,
        config: t.Optional["UntypedDict"] = None,
        unihan: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        config : dict, optional
        unihan : boolean, optional
            Bootstrap the core UNIHAN dataset (recommended)
        """
        _config: UntypedDict = config if config is not None else {}
        if config is None:
            _config = self.default_config

        # Merges custom configuration settings on top of defaults
        #: Configuration dictionary
        _config = merge_dict(self.default_config, _config)

        if unihan:
            _config = merge_dict(UNIHAN_CONFIG, _config)

        #: Expand template variables
        expand_config(_config, app_dirs)

        if not is_valid_config(config=_config):
            raise CihaiConfigError()

        self.config = _config

        user_data_dir = pathlib.Path(app_dirs.user_data_dir)

        if not user_data_dir.exists():
            user_data_dir.mkdir(parents=True)

        #: :class:`cihai.db.Database` : Database instance
        self.sql = Database(self.config)

        self.bootstrap()

    def bootstrap(self) -> None:
        for namespace, class_string in self.config.get("datasets", {}).items():
            assert isinstance(class_string, str) or (
                inspect.isclass(class_string)
                and (
                    issubclass(class_string, extend.Dataset)
                    or class_string == extend.Dataset
                )
            )
            assert isinstance(namespace, str)
            self.add_dataset(class_string, namespace)

        for dataset, plugins in self.config.get("plugins", {}).items():
            assert isinstance(dataset, str)
            assert isinstance(plugins, dict)
            for namespace, class_string in plugins.items():
                assert isinstance(namespace, str)
                assert isinstance(class_string, str) or (
                    inspect.isclass(class_string)
                    and (
                        issubclass(class_string, extend.DatasetPlugin)
                        or class_string == extend.DatasetPlugin
                    )
                )
                getattr(self, dataset).add_plugin(class_string, namespace)

    def add_dataset(self, _cls: t.Union["DS", str], namespace: str) -> None:
        if isinstance(_cls, str):
            _cls = import_string(_cls)

        assert callable(_cls)

        setattr(self, namespace, _cls())
        dataset = getattr(self, namespace)

        if isinstance(dataset, extend.SQLAlchemyMixin):
            dataset.sql = self.sql

    @classmethod
    def from_file(
        cls, config_path: t.Union[pathlib.Path, str], *args: object, **kwargs: object
    ) -> "Cihai":
        """
        Create a Cihai instance from a JSON or YAML config.

        Parameters
        ----------
        config_path : str, optional
            path to custom config file

        Returns
        -------
        :class:`Cihai` :
            application object
        """
        if isinstance(config_path, str):
            config_path = pathlib.Path(config_path)

        config = ConfigReader.from_file(path=config_path)

        return cls(config.content)
