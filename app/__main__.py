import sys

from app.clients.trivia.trivia_client_utils import get_categories
from app.arg_parser import app_parser, main_parser
from app.log import logger
from app.run import App

if __name__ == '__main__':
    main_parser = main_parser()
    options, rest = main_parser.parse_known_args()

    if options.categories_index:
        for d in get_categories():
            logger.error("%s %s", d["id"], d["name"])
        sys.exit()

    app_parser = app_parser()
    options, _s = app_parser.parse_known_args()
    app = App(
        options.trivia_api_url,
        options.transifex_api_url,
        options.transifex_token,
        options.transifex_organization,
        options.transifex_project
    )

    app.run(options.categories, options.questions_num)
