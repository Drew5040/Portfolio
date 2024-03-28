from logging import basicConfig, debug, DEBUG
from navigation import app as navigation_app
from flask import Flask
from config import Config

# Set app instance
app = Flask(__name__)

# Set session variables
app.config.from_object(Config)

# Register blueprints or apps from other modules
app.register_blueprint(navigation_app)

if __name__ == '__main__':
    # Set Logger
    basicConfig(filename='logs/flask/error.log', level=DEBUG, format='%(asctime)s - %(name)s - %('
                                                                     'levelname)s - %(message)s')
    # Log that main() is accessed
    debug('main() accessed ...')

    # Run development server
    app.run(debug=True, port=5000)
