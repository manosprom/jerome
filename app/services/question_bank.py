import json
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

from app.utils import get_project_root


class QuestionBank(object):
    def __init__(self, path: str = None):
        self._path = path
        self._store_path = self.__get_store_path()
        self.__create_store()
        self._question_bank = {}
        self.__load()

    def __create_store(self):
        Path(self._store_path).mkdir(parents=True, exist_ok=True)

    def __get_store_path(self):
        return Path(get_project_root()) / self._path if self._path else "store"

    def __get_category_path(self, category):
        return os.path.join(self.__get_store_path(), category + ".json")

    def __load(self):
        store_path = self.__get_store_path()
        files = [f for f in listdir(store_path) if isfile(join(store_path, f))]
        for file in files:
            category_path = f"{store_path}/{file}"
            category = os.path.splitext(file)[0]
            self._question_bank[category] = {}
            with open(category_path, 'r', encoding="utf-8") as category_file:
                category_data = json.load(category_file)
                self._question_bank[category] = category_data

        return self._question_bank

    def __save(self, category: str = None):
        with open(self.__get_category_path(category), 'w') as category_file:
            json.dump(self._question_bank[category], category_file, indent=4)

    def store(self, category: str, questions: []):
        if not self._question_bank.get(category):
            self._question_bank[category] = {}

        category_items = self._question_bank.get(category)
        for question in questions:
            for key, value in question.items():
                if not category_items.get(key):
                    category_items[key] = value
        self.__save(category)

    def get(self, category):
        return self._question_bank.get(category)
