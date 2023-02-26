import logging


class BullyLogging:
    def __init__(self, filename):
        logging.basicConfig(filename=filename, level=logging.INFO)

    def log_info(self, msg):
        logging.info(msg)
