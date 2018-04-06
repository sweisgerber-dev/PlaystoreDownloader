import logging

class Logger:
    @staticmethod
    def setup_logging():
        logging.basicConfig(level=logging.DEBUG, style='{', format='{message}')
        # logger = logging.getLogger()
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('{message}', style='{')
        # console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)
