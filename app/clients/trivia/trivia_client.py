import requests
import urllib.parse as url

from app.log import logger


class TriviaClient(object):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_token(self):
        params = {
            "command": "request"
        }
        response = requests.get(self.create_path("api_token.php"), params=params)
        response.raise_for_status()
        return response.json()

    def get_questions(self, amount=10, category: int = None, difficulty: str = None):
        params = self.get_questions_params(amount, category, difficulty)
        response = requests.get(self.create_path("api.php"), params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_questions_params(amount=10, category: int = None, difficulty: str = None):
        params = {
            "amount": amount
        }
        if category is not None:
            params["category"] = category

        if difficulty is not None:
            params["difficulty"] = difficulty

        return params

    def get_categories(self):
        response = requests.get(self.create_path("api_category.php"))
        response.raise_for_status()
        return response.json()

    def create_path(self, path):
        return url.urljoin(self.base_url, path)
