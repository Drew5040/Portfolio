"""
Module docstring: This module configures and initializes the Flask application and its components.
"""

from logging import basicConfig, debug, DEBUG
from gunicorn.app.base import Application
from flask import Flask
from navigation import app as navigation_app
from config import Config

# Set app instance
app = Flask(__name__)

# Set session variables
app.config.from_object(Config)

# Register blueprints or apps from other modules
app.register_blueprint(navigation_app)


class FlaskApplication(Application):
    """
    FlaskApplication configures and initializes the Gunicorn server with Flask application.
    """
    def __init__(self, parser, opts, *args):
        super().__init__(parser, opts)
        self.parser = parser
        self.opts = opts
        self.args = args

    def init(self, parser, opts, args):
        # Method should be implemented as needed
        pass

    def load(self):
        return app


if __name__ == '__main__':

    # Set Logger
    basicConfig(filename='/app/logs/flask/error.log', level=DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Log that main() is accessed
    debug('main() accessed ...')

    # Start application
    FlaskApplication(None, None).run()
