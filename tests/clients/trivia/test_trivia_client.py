import json

import pytest
import responses

from app.clients.trivia.trivia_client import TriviaClient
from tests.utils import load_test_resource


class TestTriviaClient:

    @pytest.fixture
    def trivia_client(self):
        return TriviaClient("https://trivia.api")

    @responses.activate
    def test_generate_token_should_request_for_a_trivia_session_token(self, trivia_client):
        # Given
        expected_api_token_response = json.loads(load_test_resource("clients/trivia/mocked_create_token_response.json"))

        responses.add(
            responses.GET,
            "https://trivia.api/api_token.php?command=request",
            json=expected_api_token_response,
            status=200
        )

        # When
        actual_api_token_response = trivia_client.create_token()

        # Then
        assert actual_api_token_response == expected_api_token_response

    def test_get_questions_params_without_any_filters_should_add_only_the_amount_of_questions(self):
        # Given
        amount = 10

        # When
        params = TriviaClient.get_questions_params(amount)

        # Then
        assert params == {"amount": 10}

    def test_get_questions_params_with_filters_should_add_all_requested_filters(self):
        # Given
        amount = 10
        category = 1
        difficulty = "easy"

        # When
        params = TriviaClient.get_questions_params(amount, category, difficulty)

        # Then
        assert params == {"amount": 10, "category": 1, "difficulty": "easy"}

    @responses.activate
    def test_get_questions_should_request_trivia_questions(self, trivia_client):
        # Given
        expected_questions_response = json.loads(load_test_resource("clients/trivia//mocked_get_questions_response.json"))

        responses.add(
            responses.GET,
            "https://trivia.api/api.php",
            json=expected_questions_response,
            status=200
        )

        # When
        actual_questions_response = trivia_client.get_questions()

        # Then
        assert responses.calls[0].request.url == 'https://trivia.api/api.php?amount=10'
        assert actual_questions_response == expected_questions_response
