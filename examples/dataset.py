#!/usr/bin/env python
"""Example of a custom dataset for cihai."""

import typing as t

from cihai.core import Cihai
from cihai.extend import Dataset

data = {}  # any data source, internal, a file, on the internet, in a database...


class MyDataset(Dataset):
    """Hardcoded example dataset for Cihai."""

    def bootstrap(self) -> None:  # automatically ran with .add_dataset, if exists
        """Initialize hard-coded dataset."""
        # Use this to setup your dataset, check if updates are needed, etc.
        data.update({"好": "Good", "好好": "Hello"})

    def givemedata(self, key: str) -> str:
        """Return data via direct key match."""
        return data[key]

    def search(self, needle: str) -> t.Dict[str, object]:
        """Return key-value mapping of keys matching a subset of value."""
        return {k: v for k, v in data.items() if needle in k}

    def backwards(self, needle: str) -> t.List[str]:
        """Reverse lookup."""
        return [k for k, v in data.items() if needle in v]


def run() -> None:
    """Run hard-coded example dataset."""
    c = Cihai(unihan=False)

    c.add_dataset(MyDataset, namespace="moo")
    my_dataset = MyDataset()
    my_dataset.bootstrap()


if __name__ == "__main__":
    run()
