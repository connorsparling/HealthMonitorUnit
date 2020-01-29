
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-13s) %(message)s',
                    )

def print_log(message):
    logging.debug(message)