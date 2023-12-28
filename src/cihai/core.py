"""Cihai core functionality."""

import dataclasses
import inspect
import logging
import pathlib
import typing as t

from cihai._internal.config_reader import ConfigReader
from cihai.data.unihan.dataset import Unihan

from . import exc, extend
from .config import expand_config
from .constants import DEFAULT_CONFIG, Config, UnihanConfig, app_dirs
from .db import Database
from .utils import import_string

if t.TYPE_CHECKING:
    from typing_extensions import TypeGuard

    DS = t.TypeVar("DS", bound=type[extend.Dataset])


log = logging.getLogger(__name__)


class CihaiConfigError(exc.CihaiException):
    """Cihai Configuration error."""

    def __init__(self) -> None:
        return super().__init__("Invalid exception with configuration")


def is_valid_config(config: "Config") -> "TypeGuard[Config]":
    """Upcast cihai configuration.

    NOTE: This does not validate configuration yet!
    """
    return True


class Cihai:
    """Central application object.

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
    default_config: "Config" = DEFAULT_CONFIG
    config: "Config"
    unihan: Unihan
    sql: Database

    def __init__(
        self,
        config: t.Optional[t.Union["t.Mapping[str,t.Any]", "Config"]] = None,
        unihan: bool = True,
    ) -> None:
        """Initialize Cihai application.

        Parameters
        ----------
        config : dict, optional
        unihan : boolean, optional
            Bootstrap the core UNIHAN dataset (recommended)
        """
        print(f"config 1: {t.reveal_type(config)}")

        if config is None:
            config = self.default_config
            print(f"config 2: {t.reveal_type(config)}")
        if not isinstance(config, Config):
            config = Config(**config)
            print(f"config 3: {t.reveal_type(config)}")
        print(f"config 4: {t.reveal_type(config)}")

        assert isinstance(config, Config)

        # Merges custom configuration settings on top of defaults
        #: Configuration dictionary
        config = dataclasses.replace(self.default_config, **dataclasses.asdict(config))

        if unihan:
            for dataset_name, dataset_options in UnihanConfig().datasets.items():
                if dataset_name not in config.datasets:
                    config.datasets[dataset_name] = dataset_options

        #: Expand template variables
        config = dataclasses.replace(
            config,
            **dataclasses.asdict(expand_config(config, app_dirs)),
        )
        print(f"config: {t.reveal_type(config)}")

        if not is_valid_config(config=config):
            raise CihaiConfigError
        self.config = config

        user_data_dir = pathlib.Path(app_dirs.user_data_dir)

        if not user_data_dir.exists():
            user_data_dir.mkdir(parents=True)

        #: :class:`cihai.db.Database` : Database instance
        self.sql = Database(self.config)

        self.bootstrap()

    def bootstrap(self) -> None:
        """Initialize Cihai."""
        for dataset_name, class_string in self.config.datasets.items():
            assert isinstance(class_string, str) or (
                inspect.isclass(class_string)
                and (
                    issubclass(class_string, extend.Dataset)
                    or class_string == extend.Dataset
                )
            )
            assert isinstance(dataset_name, str)
            self.add_dataset(class_string, namespace=dataset_name)

        for plugin_name, plugin_dict in self.config.plugins.items():
            assert isinstance(plugin_name, str)
            assert isinstance(plugin_dict, dict)
            if "options" in plugin_dict:
                assert isinstance(plugin_dict["options"], dict)
                for option_name, class_string in plugin_dict["options"].items():
                    assert isinstance(option_name, str)
                    assert isinstance(class_string, str) or (
                        inspect.isclass(class_string)
                        and (
                            issubclass(class_string, extend.DatasetPlugin)
                            or class_string == extend.DatasetPlugin
                        )
                    )
                    print(f"option_name: {option_name}")
                    print(f"class string: {class_string}")
                    getattr(self, plugin_name).add_plugin(class_string, plugin_name)

    def add_dataset(self, cls: t.Union["DS", str], namespace: str) -> None:
        """Add dataset to Cihai."""
        if isinstance(cls, str):
            cls = import_string(cls)

        assert callable(cls)

        setattr(self, namespace, _cls(cihai=self))
        dataset = getattr(self, namespace)

        if isinstance(dataset, extend.SQLAlchemyMixin):
            dataset.sql = self.sql

    @classmethod
    def from_file(
        cls,
        config_path: t.Union[pathlib.Path, str],
        *args: object,
        **kwargs: object,
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
