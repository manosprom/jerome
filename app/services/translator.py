from hashlib import md5

from requests import HTTPError

from app.log import logger
from app.services.translator_utils import slugify


class Translator(object):
    def __init__(self, transifex_client, question_bank):
        self.transifex_client = transifex_client
        self.question_bank = question_bank

    def request_translations(self, category_name: str, trivia_questions: []):
        logger.info(f"Sending questions for translation ({category_name})")
        escaped_category_name = slugify(category_name)
        prepare_questions = self.prepare_questions_for_translation(trivia_questions)
        self.question_bank.store(escaped_category_name, prepare_questions)
        items_for_translation = self.question_bank.get(escaped_category_name)
        self.get_or_create_resource(escaped_category_name)
        self.transifex_client.resource_strings_upload(escaped_category_name, items_for_translation)
        logger.info(f"Questions uploaded for translation ({category_name})")

    def get_or_create_resource(self, category):
        logger.debug(f"Check if transifex resource already exists for {category}")
        try:
            resource = self.transifex_client.get_resource(category)
            logger.debug(f"resource already exists for {category}")
        except HTTPError as http_error:
            if http_error.response.status_code == 404:
                resource = self.transifex_client.create_resource(category)
                logger.debug(f"resource created for {category}")
            else:
                raise http_error

        return resource

    def prepare_questions_for_translation(self, questions: []):
        prepared_questions = []
        for question in questions:
            prepared_question = self.prepare_question(question)
            prepared_questions.append(prepared_question)
        return prepared_questions

    @staticmethod
    def prepare_question(question):
        prepared_question = {}
        question_hash = Translator.generate_hash(question["question"])
        correct_answer_hash = Translator.generate_hash(question["correct_answer"])
        prepared_question[f"q_{question_hash}"] = question["question"]
        counter = 0
        prepared_question[f"q_{question_hash}_a{counter}_{correct_answer_hash}"] = question["correct_answer"]
        for incorrect_answer in question["incorrect_answers"]:
            counter += 1
            incorrect_answer_hash = Translator.generate_hash(incorrect_answer)
            prepared_question[f"q_{question_hash}_a{+counter}_{incorrect_answer_hash}"] = incorrect_answer
        return prepared_question

    @staticmethod
    def generate_hash(source_string: str):
        keys = [source_string, '']

        return md5(':'.join(keys).encode('utf-8')).hexdigest()

    @staticmethod
    def clean_text(source_string: str):
        source_string = source_string.replace('\\', '\\\\')
        source_string = source_string.replace('.', r'\.')
        return source_string
