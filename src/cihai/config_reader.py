import json
import pathlib

import yaml


class ConfigReader:
    def __init__(self, path: pathlib.Path):
        self.config_path = path

    def import_config(self):
        path = self.config_path
        content = open(path).read()
        if path.suffix in [".yaml", ".yml"]:
            return yaml.load(content, Loader=yaml.Loader)
        elif path.suffix == ".json":
            return json.loads(content)
        else:
            raise NotImplementedError(f"{path.suffix} not supported in {path}")
