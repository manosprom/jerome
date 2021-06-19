import unittest

from unittest.mock import MagicMock, patch
from app.clients.trivia.trivia_client_utils import get_category_name, parse_categories


class TestTriviaCategories:

    @patch("app.clients.trivia.trivia_client_utils.get_categories")
    def test_get_category_name_should_return_the_category_name_when_category_exists(self, get_categories_mock):
        # Given
        given_categories = [
            {
                "id": 9,
                "name": "General Knowledge"
            },
            {
                "id": 10,
                "name": "Entertainment: Books"
            }
        ]

        get_categories_mock.return_value = given_categories

        # When
        expected_category_id = get_category_name(9)

        # then
        assert expected_category_id == "General Knowledge"

    @patch("app.clients.trivia.trivia_client_utils.get_categories")
    def test_get_category_id_should_return_none_when_category_not_found(self, get_categories_mock):
        # Given
        given_categories = [
            {
                "id": 9,
                "name": "General Knowledge"
            },
            {
                "id": 10,
                "name": "Entertainment: Books"
            }
        ]
        get_categories_mock.return_value = given_categories

        # When
        expected_category_id = get_category_name(0)

        # then
        assert expected_category_id is None

    @patch("app.clients.trivia.trivia_client_utils.get_categories")
    def test_get_category_id_should_return_the_first_occurrence(self, get_categories_mock):
        # Given
        given_categories = [
            {
                "id": 10,
                "name": "Category 1"
            },
            {
                "id": 10,
                "name": "Category 2"
            }
        ]
        get_categories_mock.return_value = given_categories

        # When
        expected_category_id = get_category_name(10)

        # then
        assert expected_category_id == "Category 1"

    @patch("app.clients.trivia.trivia_client_utils.get_categories")
    def test_parse_categories_should_return_id_to_name_mapping(self, get_categories_mock):
        # Given
        given_categories = [
            {
                "id": 10,
                "name": "Category 1"
            },
            {
                "id": 10,
                "name": "Category 2"
            }
        ]
        get_categories_mock.return_value = given_categories

        # When
        category_mapping = parse_categories([10])

        # then
        assert category_mapping == {
            10: "Category 1"
        }
