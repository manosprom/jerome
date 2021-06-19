import logging

console_handler = logging.StreamHandler()
logger = logging.getLogger()
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)