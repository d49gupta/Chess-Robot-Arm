import logging

def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(name + '_logs.csv', mode = 'w')
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def set_logger_level(logger, level):
    logger.setLevel(level)