from app.services.question_bank import QuestionBank


class TestQuestionBank:

    def test_load_should_load_existing_questions(self):
        # Given
        question_bank = QuestionBank(path='../tests/services/store')

        # When
        category_1 = question_bank.get(category="category_1")
        category_2 = question_bank.get(category="category_2")

        # Then
        assert len(category_1) == 5
        assert category_1["q_439a579dea9730068b21dfe00d957a25"] == "question_category_1"
        assert category_1["q_439a579dea9730068b21dfe00d957a25_a0_654a9672469401ce8348a194f7c5e329"] == "question_category_1_correct_answer"
        assert category_1["q_439a579dea9730068b21dfe00d957a25_a1_15e8bfff2c10ca22da244d85b2bf7d94"] == "question_category_1_wrong_answer_1"
        assert category_1["q_439a579dea9730068b21dfe00d957a25_a2_243f63354f4c1cc25d50f6269b844369"] == "question_category_1_wrong_answer_2"
        assert category_1["q_439a579dea9730068b21dfe00d957a25_a3_da64a1bc2c9a53dd1cdb6846103cd2de"] == "question_category_1_wrong_answer_3"

        assert len(category_2) == 5
        assert category_2["q_439a579dea9730068b21dfe00d957a25"] == "question_category_2"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a0_654a9672469401ce8348a194f7c5e329"] == "question_category_2_correct_answer"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a1_15e8bfff2c10ca22da244d85b2bf7d94"] == "question_category_2_wrong_answer_1"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a2_243f63354f4c1cc25d50f6269b844369"] == "question_category_2_wrong_answer_2"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a3_da64a1bc2c9a53dd1cdb6846103cd2de"] == "question_category_2_wrong_answer_3"

    def test_merge_should_not_add_items_if_same_key_exists(self):
        # Given
        question_bank = QuestionBank(path='../tests/services/store')

        new_questions = [
            {
                "q_439a579dea9730068b21dfe00d957a25": "question_category_2",
                "q_439a579dea9730068b21dfe00d957a25_a0_654a9672469401ce8348a194f7c5e329": "question_category_2_correct_answer",
                "q_439a579dea9730068b21dfe00d957a25_a1_15e8bfff2c10ca22da244d85b2bf7d94": "question_category_2_wrong_answer_1",
                "q_439a579dea9730068b21dfe00d957a25_a2_243f63354f4c1cc25d50f6269b844369": "question_category_2_wrong_answer_2",
                "q_439a579dea9730068b21dfe00d957a25_a3_da64a1bc2c9a53dd1cdb6846103cd2de": "question_category_2_wrong_answer_3"
            }
        ]

        # When
        question_bank.store("category_2", new_questions)

        # Then
        category_1 = question_bank.get("category_1")
        category_2 = question_bank.get("category_2")

        assert len(category_1) == 5

        assert len(category_2) == 5
        assert category_2["q_439a579dea9730068b21dfe00d957a25"] == "question_category_2"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a0_654a9672469401ce8348a194f7c5e329"] == "question_category_2_correct_answer"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a1_15e8bfff2c10ca22da244d85b2bf7d94"] == "question_category_2_wrong_answer_1"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a2_243f63354f4c1cc25d50f6269b844369"] == "question_category_2_wrong_answer_2"
        assert category_2["q_439a579dea9730068b21dfe00d957a25_a3_da64a1bc2c9a53dd1cdb6846103cd2de"] == "question_category_2_wrong_answer_3"
