from sys import stderr
from logging import getLogger, Formatter, StreamHandler, getLevelName
from logging.handlers import RotatingFileHandler


def initialize_log():
    # Create a logger object
    logr = getLogger('web.logger')

    # Set logging level from env vars or default to DEBUG
    log_level = getLevelName('DEBUG')

    # Set the level of the logger object
    logr.setLevel(log_level)

    # Create the formatter object
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a rotating file handler object
    file_handler = RotatingFileHandler(
        filename='logs/flask/error.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Create a stream handler for stderr to print logs to console
    stream_handler = StreamHandler(stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    # Add both handlers to the logger object
    logr.addHandler(file_handler)
    logr.addHandler(stream_handler)

    return logr


logger = initialize_log()
