"""
log_config.py

This module provides a centralized logging configuration for the Flask application.

It sets up structured JSON logging which outputs to standard output (stdout). This setup facilitates easy integration

with external log management tools and ensures that log output is both human-readable and machine-parseable.

The logger can be configured via an environment variable (`LOGGING_LEVEL`) to adjust the verbosity of the logs. If not

specified, it defaults to DEBUG level. The logs are formatted in JSON to include the timestamp, log level, logger name,

and message content.

Functions:
    initialize_log() -> logging.Logger: Initializes and returns a configured logger.
"""

from logging import DEBUG, getLogger
from os import getenv
from sys import stdout
from logging import StreamHandler, getLevelName
from celery.signals import setup_logging
from pythonjsonlogger import jsonlogger


@setup_logging.connect
def initialize_log(**kwargs):
    """
        Initializes and configures the logging system for the application.

        The function configures a root logger to output JSON formatted log messages to standard output. It uses the

        environment variable 'LOGGING_LEVEL' to set the logging level; if not specified, it defaults to DEBUG.

        The JSON format is achieved using the pythonjsonlogger library, which transforms standard log messages into

        JSON.

        Error Handling:
            In case of any configuration error (e.g., incorrect logging level name), the function logs an error message
            to the root logger and returns `None`.

        Returns:
            logging.Logger: A configured logger object ready for use, or None if an error occurred during setup.
        """

    try:
        # Use Flask's native logger
        logr = getLogger()

        # Set the logging level from the environment variable or default to DEBUG
        log_level = getenv("LOGGING_LEVEL", "INFO")

        # Grab the numeric level
        numeric_level = getLevelName(log_level)

        # Ensure numeric is returned from getLevelName()
        if not isinstance(numeric_level, int):
            numeric_level = getenv('LOGGING_LEVEL')

        # Set the logr level
        logr.setLevel(numeric_level)

        # Create a formatter object
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt='%Y-%m-%dT%H:%M:%S'
        )

        # Create a stream handler for stdout
        stdout_handler = StreamHandler(stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(numeric_level)

        # Add the handler to the logger
        if not any(isinstance(handler, StreamHandler) for handler in logr.handlers):
            logr.addHandler(stdout_handler)

        return logr
    except Exception as e:
        logger.error(f'Failed to initialize logger: {e}')
        return None


logger = initialize_log()
