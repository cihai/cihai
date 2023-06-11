#!/usr/bin/env python
import typing as t

from cihai.core import Cihai
from cihai.extend import Dataset

data = {}  # any data source, internal, a file, on the internet, in a database...


class MyDataset(Dataset):
    def bootstrap(self) -> None:  # automatically ran with .add_dataset, if exists
        # Use this to setup your dataset, check if updates are needed, etc.
        data.update({"好": "Good", "好好": "Hello"})

    def givemedata(self, key: str) -> str:
        return data[key]

    def search(self, needle: str) -> t.Dict[str, object]:
        return {k: v for k, v in data.items() if needle in k}

    def backwards(self, needle: str) -> t.List[str]:
        return [k for k, v in data.items() if needle in v]


def run() -> None:
    c = Cihai(unihan=False)

    c.add_dataset(MyDataset, namespace="moo")
    my_dataset = MyDataset()
    my_dataset.bootstrap()

    print("Definitions exactly for 好", my_dataset.givemedata("好"))

    print("Definitions matching with 你好:", ", ".join(my_dataset.search("好")))

    print("Reverse definition with Good:", ", ".join(my_dataset.backwards("Good")))


if __name__ == "__main__":
    run()
