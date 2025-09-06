import logging

def get_logger(name):
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(asctime)s:%(name)s:%(message)s")
    return logging.getLogger(name)
