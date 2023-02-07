import logging

logger = None


def init(name='gpt3.chatbot'):
    global logger

    if logger is None:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
    else:
        return logger
