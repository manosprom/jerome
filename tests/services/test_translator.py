from unittest.mock import MagicMock

import pytest

from app.services.translator import Translator


class TestTranslator:

    @pytest.fixture
    def transifex_client_mock(self):
        return MagicMock()

    @pytest.fixture
    def question_bank_mock(self):
        return MagicMock()

    @pytest.fixture
    def translator(self, transifex_client_mock, question_bank_mock):
        return Translator(transifex_client=transifex_client_mock, question_bank=question_bank_mock)

    def test_clean_text_should_escape_backslash_and_dots(self):
        # Given
        text = r"\something."

        # When
        clean_text = Translator.clean_text(text)

        # Then
        assert clean_text == r"\\something\."

    def test_generate_hash(self):
        hashed = Translator.generate_hash(r"\\something\.")
        assert hashed == "006e127ff43db320b01c4fc35fe2707a"

    def test_prepare_question_should_convert_a_trivia_question(self, translator):
        # Given
        trivia_question = {
            "category": "Entertainment: Japanese Anime & Manga",
            "type": "multiple",
            "difficulty": "easy",
            "question": "What is the name of the corgi in Cowboy Bebop?",
            "correct_answer": "Einstein",
            "incorrect_answers": [
                "Edward",
                "Rocket",
                "Joel"
            ]
        }

        # When
        prepared_question = Translator.prepare_question(trivia_question)

        # Then
        assert prepared_question['q_17e555825577daf7bc97585ba3ec8e04'] == 'What is the name of the corgi in Cowboy Bebop?'
        assert prepared_question['q_17e555825577daf7bc97585ba3ec8e04_a0_f1eaa6788d5ce78abbc1f962d4af140d'] == 'Einstein'
        assert prepared_question['q_17e555825577daf7bc97585ba3ec8e04_a1_86f8dc25e6683dfcb35e20a1e3fb9c76'] == 'Edward'
        assert prepared_question['q_17e555825577daf7bc97585ba3ec8e04_a2_1b94b28eb1e0896af63f7deeb84d9be4'] == 'Rocket'
        assert prepared_question['q_17e555825577daf7bc97585ba3ec8e04_a3_8b0b4f8aff8ef3700dbe3dfa0fc4c7d8'] == 'Joel'

    def test_request_translation_should_prepare_and_send_trivia_for_translations(self, translator, transifex_client_mock, question_bank_mock):
        # Given
        category = "entertainment"
        trivia_question = {
            "category": "Entertainment: Japanese Anime & Manga",
            "type": "multiple",
            "difficulty": "easy",
            "question": "What is the name of the corgi in Cowboy Bebop?",
            "correct_answer": "Einstein",
            "incorrect_answers": [
                "Edward",
                "Rocket",
                "Joel"
            ]
        }
        prepared_questions = translator.prepare_questions_for_translation(questions = [trivia_question])

        # When
        translator.request_translations(category, [trivia_question])

        # Then
        transifex_client_mock.get_resource.assert_called_once()
        transifex_client_mock.get_resource.assert_called_with(category)

        question_bank_mock.store.assert_called_once()
        question_bank_mock.store.assert_called_with('entertainment', prepared_questions)

        transifex_client_mock.resource_strings_upload("entertainment", prepared_questions)
