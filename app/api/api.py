from flask import Flask
from clients.trivia.trivia_client import TriviaClient

api = Flask(__name__)

client = TriviaClient("https://opentdb.com")


@api.route('/questions', methods=["GET"], )
def get_questions():
    return client.get_questions(10)


@api.route('/categories', methods=["GET"])
def get_categories():
    return client.get_categories()
