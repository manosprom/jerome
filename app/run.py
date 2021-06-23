from app.clients.transifex.transifex_client import TransifexClient
from app.clients.trivia.trivia_client import TriviaClient
from app.clients.trivia.trivia_client_utils import parse_categories
from app.log import logger
from app.services.question_bank import QuestionBank
from app.services.translator import Translator


class App(object):
    def __init__(
            self,
            trivia_url: str,
            transifex_url,
            transifex_token,
            transifex_organization,
            transifex_project
    ):
        logger.info("---------------------------------------------------")
        logger.info("Initializing app with: ")
        logger.info("trivia_url: %s", trivia_url)
        logger.info("transifex_url: %s", transifex_url)
        logger.info("transifex_token: %s", transifex_token)
        logger.info("transifex_organization: %s", transifex_organization)
        logger.info("transifex_project: %s", transifex_project)
        logger.info("---------------------------------------------------")

        self.trivia_client = TriviaClient(base_url=trivia_url)
        self.transifex_client = TransifexClient(
            base_url=transifex_url,
            token=transifex_token,
            organization=transifex_organization,
            project=transifex_project,
        )

        self.question_bank = QuestionBank(path=None)

        self.translator = Translator(
            transifex_client=self.transifex_client,
            question_bank=self.question_bank
        )

    def run(self, category_ids: [str], question_num: int = 10):
        if not category_ids:
            logger.info("Please specify at least one category")
            return

        logger.info(f"Fetching questions for categories {category_ids}")

        try:
            categories = parse_categories(category_ids=category_ids)
        except Exception as ex:
            logger.error(str(ex))
            return

        for category_id, category_name in categories.items():
            logger.info(f"Fetching {question_num} questions for category {category_name}")
            questions = self.trivia_client.get_questions(amount=question_num, category=category_id)
            logger.info(f"Fetched {question_num} questions for category {category_name}")
            self.translator.request_translations(category_name, questions['results'])

        logger.info("---------------------------------------------------")
        logger.info("You can view and translate your questions on transifex site.")
