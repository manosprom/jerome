from argparse import ArgumentParser


def main_parser():
    description = (
        """
        Show the categories if requiested
        """
    )
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--categories-index",
        action="store_true",
        dest="categories_index",
        help="The categories index to select from.",
    )

    return parser


def app_parser():
    description = (
        """
        A simple command line application to request some questions for some categories from trivia api
        and request upload the questions to be translated on transifex.
        """
    )
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--transifex-api-url",
        action="store",
        type=str,
        dest="transifex_api_url",
        default="https://rest.api.transifex.com",
        help="The transifex api host"
    )

    parser.add_argument(
        "--transifex-token",
        action="store",
        dest="transifex_token",
        default=None,
        help="Transifex Api token i.e 1/caeoejraecnear14134afaer6rfs",
        required=True
    )

    parser.add_argument(
        "--transifex-organization",
        action="store",
        dest="transifex_organization",
        default=None,
        help="Transifex Organization i.e jerome-2 (This should be created from the site.",
        required=True
    )

    parser.add_argument(
        "--transifex-project",
        action="store",
        dest="transifex_project",
        default=None,
        help="Transifex ProjectId i.e jerome-translator (This should be created from the site)",
        required=True
    )

    parser.add_argument(
        "--trivia-api-url",
        action="store",
        dest="trivia_api_url",
        default="https://opentdb.com",
        help="Trivia api url"
    )

    parser.add_argument(
        "-c"
        "--categories",
        action="store",
        dest="categories",
        default=[],
        nargs="+",
        type=int,
        help="The categories to request.",
        required=True
    )

    parser.add_argument(
        "--questions-num",
        action="store",
        dest="questions_num",
        default=10,
        help="The number of questions to request."
    )

    return parser
