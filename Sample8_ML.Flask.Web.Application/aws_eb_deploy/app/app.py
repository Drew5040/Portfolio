"""
app.py

This module configures and initializes the Flask application and its components.
"""

from json import dumps
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from gunicorn.app.base import Application
from config import Config
from helper import value_predictor, validate_form_entries
from log_config import logger
from error_config import register_error_handlers
from celery_config import make_celery
from redis_config import rate_limiter
from content import (

    Metadata, NavigationLink, Footer,
    WelcomePage, AboutPage,
    ModelPage, ContactSubmissions

)

# Set app instance
app = Flask(
    import_name=__name__,
    template_folder='templates',
    static_folder='static'
)

# Log that app is instantiated
logger.info("Flask() configured...")

# Register error handlers
register_error_handlers(app)

# Set session variables
app.config.from_object(obj=Config)

# Log that environment variables have been configured
logger.info(msg="Environment variables configured...")

# Create & connect PostgreSQL database instance
db = SQLAlchemy(app)

# Log sqlalchemy configured
logger.info(msg="SQLAlchemy() configured...")

# Initialize Celery queue
celery = make_celery(app)

# Log Celery queue is initialized
logger.info(msg='Celery() initialized...')


# Set Context Processor
@app.context_processor
def common_data():
    """View provides constant data from PostgreSQL database
       to all .html templates"""

    # Log
    logger.info(msg='Context_processor() accessed ...')

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
@app.route(rule='/', methods=['GET'])
def home_page():
    """Homepage of web application"""

    # Log
    logger.info(msg='Home_page() accessed ... ')

    # Request data from PostgreSQL database and make available to welcome.html
    welcome_page_data = db.session.query(WelcomePage).first()

    # Render the page with the data
    return render_template(template_name_or_list='welcome.html', welcome_page_data=welcome_page_data)


@app.route(rule='/about', methods=['GET'])
def about_page():
    """About page of web application"""

    # Log
    logger.info('About_page() accessed ...')

    # Grab about_page data
    about_page_data = db.session.query(AboutPage).first()

    # Render the page
    return render_template(template_name_or_list='about.html', about_page_data=about_page_data)


# Display prediction
@app.route(rule='/model', methods=['GET', 'POST'])
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

        # Log that form data was transferred to dict()
        logger.debug(msg="Form data to_dict()...")

        # Validate all entries in the form
        boole, errors, form_data = validate_form_entries(form_data=form_data)

        # If at least one invalid form entry
        if not boole:
            # Log
            logger.debug(msg='Invalid model form entry(ies) detected ...')

            # Serialize user entered form data into JSON
            errors_json = dumps(obj=errors)

            # Re-render the page because of error in form
            return render_template(template_name_or_list='model.html',
                                   form_data=form_data,
                                   errors_json=errors_json,
                                   error_message='**Please fill out all required fields**',
                                   model_page_data=model_page_data)

        # Transform user inputs into a list from the form data dict
        to_predict_list = list(form_data.values())

        # Ensure all values are integers
        to_predict_list = list(map(int, to_predict_list))

        # Log
        logger.info(msg=f'Received input for prediction: {to_predict_list}')

        # Run data through Decision Tree model
        results = value_predictor(to_predict_list=to_predict_list)

        # If the result is a 1
        if int(results) == 1:
            prediction = "**Income more than 50K**"

        # If the result is a 0
        else:
            prediction = "**Income less than 50K**"

        # Log prediction results
        logger.info(msg=f'Prediction result: {prediction}')

        # Log results are rendered
        logger.info(msg='Results rendered ...')

        # Render the model.html template with results
        return render_template(template_name_or_list='model.html', prediction=prediction,
                               model_page_data=model_page_data)

    # Log default rendering of template
    logger.info(msg='Default model.html rendering')

    # If no other return has been executed
    return render_template(template_name_or_list='model.html', model_page_data=model_page_data)


@app.route(rule='/contact', methods=['GET', 'POST'])
def contact_page():
    """Contact page view that uses the SMTP protocol
       to send emails from contact page"""

    # Log the contact page was accessed
    logger.info(msg="Contact_page() accessed ...")
    logger.debug(msg="Headers: {request.headers}")
    logger.debug(msg="Form data: {request.form}")

    # Conditions and implementations of 'POST' request
    if request.method == 'POST':

        # Grab form data
        sender = request.form['email']
        name = request.form['name']
        subject = request.form['subject']
        message = request.form['message']

        # Validate form data
        if not sender or not name or not subject or not message:
            flash(message="All fields are required", category="error")
            return render_template(template_name_or_list='contact.html')

        # Log that validation is taking place
        logger.info(msg='Contact form data grabbed...')

        # Insert data into ContactSubmissions table
        new_contact_submission = ContactSubmissions(
            email=sender,
            name=name,
            subject=subject,
            message=message
        )

        db.session.add(instance=new_contact_submission)
        db.session.commit()

        # Log that the form data is added to the database
        logger.info(msg="Form data added to database...")

        # Check rate limits before sending email
        if not rate_limiter(fapp=app, key="email_rate", limit=30, duration=60):
            flash(message='Rate limit exceeded. Please try again later.', category='error')
            return redirect(location=url_for(endpoint='contact_page'))

        # Queue the email with an execution rate of 30 msg/min
        celery.send_task(name='send_email_task', args=[sender, name, subject, message], queue='email')

        # Log the msg was sent
        logger.info(msg="Msg was sent!")

        # Flash success msg
        flash(message='Your message has been sent successfully.', category='success')

        return redirect(location=url_for(endpoint='contact_page'))

    # Log default action of page
    logger.debug(msg="Default contact.html rendering")

    return render_template(template_name_or_list='contact.html')


@app.route('/health')
def health():
    """Health view that lets AWS know the application's status"""
    logger.info(msg='Health ok...')
    return 'OK', 200


class FlaskApplication(Application):
    """
    FlaskApplication configures and initializes the Gunicorn server with Flask application.
    """

    # Log that gunicorn class is accessed
    logger.info(msg="FlaskApplication class accessed....")

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
        logger.info(msg='Instance of Flask app returned...')
        return app


if __name__ == '__main__':
    # Log that main() is accessed
    logger.info(msg='main() accessed ...')

    # Start application
    FlaskApplication(None, None).run()
    # app.run(debug=True, host='127.0.0.1', port=5000)
