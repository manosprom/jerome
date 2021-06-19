import os
from pathlib import Path


def load_test_resource(path: str):
    print(__file__)
    with open(Path(os.path.dirname(os.path.realpath(__file__))) / path, 'r', encoding="utf-8") as file:
        return file.read()
