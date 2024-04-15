"""
Module docstring: This module configures and initializes the Flask application and its components.
"""

import sys
from os import getenv, environ
from json import dumps
from email.message import EmailMessage
from smtplib import SMTPAuthenticationError, SMTP
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from gunicorn.app.base import Application
from redis import Redis
from config import Config
from helper import value_predictor, validate_form_entries
from log_config import logger
from error_config import register_error_handlers

from content import (

    Metadata, NavigationLink, Footer,
    WelcomePage, AboutPage,
    ModelPage, ContactSubmissions

)

# Set app instance
app = Flask(__name__)
logger.info("FLASK APP configured")

# Register error handlers
register_error_handlers(app)

# Set session variables
app.config.from_object('config.Config')

# Create & connect PostgreSQL database instance
db = SQLAlchemy(app)
logger.info("SqlAlchemy configured...")

# Initialize the Limiter with explicit parameters from the app config
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379",
    default_limits=[getenv('RATELIMIT_DEFAULT')]
)

# Log the rate limiter object is instantiated
logger.info("Limiter configured")

# Set up Redis connection
redis = Redis(host='localhost', port=6379, db=0)

# Log that Redis is configured
logger.info("Redis configured")

# Set Context Processor
@app.context_processor
def common_data():
    """View provides constant data from PostgreSQL database
       to all .html templates"""

    # Log
    logger.info('Context_processor() accessed ...')

    # Request data that is constant throughout application & make available for all views
    metadata = db.session.query(Metadata).filter_by(page='index').all()
    navigation_links = db.session.query(NavigationLink).all()
    footer = db.session.query(Footer).first()

    # Return constant data to all view functions
    return {
        'metadata': metadata,
        'navigation_links': navigation_links,
        'footer': footer
    }

# Set homepage route
@app.route('/')
def home_page():
    """Homepage of web application"""

    # Log
    logger.info('Home_page() accessed ... ')

    # Request data from PostgreSQL database and make available to welcome.html
    welcome_page_data = db.session.query(WelcomePage).first()

    # Render the page with the data
    return render_template('welcome.html', welcome_page_data=welcome_page_data)


@app.route('/about')
def about_page():
    """About page of web application"""

    # Log
    logger.info('About_page() accessed ...')

    # Request data from PostgreSQL tables & make available to about.html
    metadata = db.session.query(Metadata).filter_by(page='index').all()
    navigation_links = db.session.query(NavigationLink).all()
    about_page_data = db.session.query(AboutPage).first()
    footer = db.session.query(Footer).first()

    # Render the page
    return render_template('about.html', about_page_data=about_page_data)


# Display prediction
@app.route('/model', methods=['GET', 'POST'])
def result():
    """Model page view that generates results from Decision Tree model"""

    logger.debug("Model page is accessed...")
    logger.debug(f"Headers: {request.headers}")
    logger.debug(f"Form data: {request.form}")

    # Request data from PostgreSQL database & make available to model.html
    model_page_data = db.session.query(ModelPage).first()
    logger.debug("Model page data is retrieved from psql...")

    # If user hits submit on model.html
    if request.method == 'POST':

        # Grab user entered form data and store in a dict
        form_data = request.form.to_dict()

        # Log that form data was transfered to dict()
        logger.debug("Form data to_dict()...")

        # Validate all entries in the form
        boole, errors, form_data = validate_form_entries(form_data)

        # If at least one invalid form entry
        if not boole:
            # Log
            logger.debug('Invalid model form entry(ies) detected ...')

            # Serialize user entered form data into JSON
            errors_json = dumps(errors)

            # Re-render the page because of error in form
            return render_template('model.html',
                                   form_data=form_data,
                                   errors_json=errors_json,
                                   error_message='**Please fill out all required fields**',
                                   model_page_data=model_page_data)

        # Transform user inputs into a list from the form data dict
        to_predict_list = list(form_data.values())

        # Ensure all values are integers
        to_predict_list = list(map(int, to_predict_list))

        # Log
        logger.info('Received input for prediction: %s', to_predict_list)

        # Run data through Decision Tree model
        results = value_predictor(to_predict_list)

        # If the result is a 1
        if int(results) == 1:
            prediction = "**Income more than 50K**"

        # If the result is a 0
        else:
            prediction = "**Income less than 50K**"

        # Log prediction results
        logger.info('Prediction result: %s', prediction)

        # Log results are rendered
        logger.info('Results rendered ...')

        # Render the model.html template with results
        return render_template('model.html', prediction=prediction, model_page_data=model_page_data)

    # Log default rendering of template
    logger.info('Default model.html rendering')

    # If no other return has been executed
    return render_template('model.html', model_page_data=model_page_data)


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    """Contact page view that uses the SMTP protocol
       to send emails from contact page"""

    # Log the contact page was accessed
    logger.info("Contact_page() accessed ...")

    # Conditions and implementations of 'POST' request
    if request.method == 'POST':

        # Grab form data
        sender = request.form['email']
        name = request.form['name']
        subject = request.form['subject']
        message = request.form['message']

        try:

            # Validate form data
            if not sender or not name or not subject or not message:
                raise ValueError("All fields are required")

            # Log that validation is taking place
            logger.info('Contact form data grabbed ...')

            # Insert data into ContactSubmissions table
            new_contact_submission = ContactSubmissions(
                email=sender,
                name=name,
                subject=subject,
                message=message
            )

            db.session.add(new_contact_submission)
            db.session.commit()

            # Log that the form data is added to the database
            logger.info("Form data added to database ...")

            # Create EmailMessage object
            msg = EmailMessage()
            msg['From'] = getenv("EMAIL_USERNAME")
            msg['Reply-To'] = sender
            msg['To'] = getenv("EMAIL_USERNAME")
            msg['Subject'] = subject

            # Log the msg object was created
            logger.info("Message object created")

            # Set the content of the email
            msg.set_content(f'Name: {name} <{sender}>\n\n{message}')

            # Send the email
            with SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                logger.debug('TLS initiated...')
                server.login(getenv("EMAIL_USERNAME"), getenv('WEB_APP_SECRET'))
                logger.debug('Server login successful...')
                server.sendmail(getenv("EMAIL_USERNAME"), getenv("EMAIL_USERNAME"), msg.as_string())
                logger.debug("email was sent ...")
                server.quit()

            # Set message to be displayed when email is sent successfully
            flash('Your message has been sent successfully.', 'success')

            return redirect(url_for('contact_page'))

        except SMTPAuthenticationError as e:

            # Set message to be displayed when email is not successfully sent
            flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('contact_page'))

    # Log default action of page
    logger.debug("Default contact.html rendering")

    return render_template('contact.html')



@app.route('/health')
def health():
    """Health view that lets AWS know the application's status"""
    logger.info('Health ok...')
    return 200, 'OK'


class FlaskApplication(Application):
    """
    FlaskApplication configures and initializes the Gunicorn server with Flask application.
    """

    # Log that gunicorn class is accessed
    logger.info("FlaskApplication class accessed....")

    def __init__(self, parser, opts, *args):
        super().__init__(parser, opts)
        self.parser = parser
        self.opts = opts
        self.args = args

    def init(self, parser, opts, args):
        pass

    def load(self):
        """Returns an instance of the Flask application"""
        # Log the Flask app instance is returned
        logger.info('Instance of Flask app returned...')
        return app


if __name__ == '__main__':

    # Log that main() is accessed
    logger.info('main() accessed ...')

    # Start application
    FlaskApplication(None, None).run()

