from aws_eb_deploy.log_config import DEBUG, getLogger, Formatter
from aws_eb_deploy.log_config import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from os import getenv, environ
from flask import redirect, url_for, request, render_template, flash
from email.message import EmailMessage
from smtplib import SMTPAuthenticationError, SMTP
from json import dumps
from content import Metadata, NavigationLink, Footer, WelcomePage, AboutPage, ModelPage, ContactSubmissions
from helper import value_predictor, validate_form_entries

# Set app instance
app = Flask(__name__)

# Set session variables
app.config.from_object(Config)

# Connect PostgreSQL database
environ["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")

# Create SQLAlchemy database instance
db = SQLAlchemy(app)


# Set Context Processor
@app.context_processor
def common_data():
    # Log
    logger.debug('Context_processor() accessed ...')

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
    # Log
    logger.debug('Home_page() accessed ... ')

    # Request data from PostgreSQL database and make available to welcome.html
    welcome_page_data = db.session.query(WelcomePage).first()

    # Render the page with the data
    return render_template('welcome.html', welcome_page_data=welcome_page_data)


@app.route('/about')
def about_page():
    # Log
    logger.debug('about_page() accessed ...')

    # Request data from PostgreSQL tables & make available to about.html

    about_page_data = db.session.query(AboutPage).first()

    # Render the page
    return render_template('about.html', about_page_data=about_page_data)


# Display prediction
@app.route('/model', methods=['GET', 'POST'])
def result():
    # Request data from PostgreSQL database & make available to model.html
    model_page_data = db.session.query(ModelPage).first()

    # If user hits submit on model.html
    if request.method == 'POST':

        # Grab user entered form data and store in a dict
        form_data = request.form.to_dict()

        # Validate all entries in the form
        boole, errors, form_data = validate_form_entries(form_data)

        # If at least one invalid form entry
        if not boole:
            # Log
            logger.debug('Invalid entry(ies) detected ...')

            # Serialize user entered form data into JSON data & pass data back to the template (model.html)
            errors_json = dumps(errors)

            # Re-render the page because of error in form
            return render_template('model.html',
                                   form_data=form_data,
                                   errors_json=errors_json,
                                   error_message='**Please fill out all required fields**',
                                   model_page_data=model_page_data)

        # If there are no errors in the form data transform user inputs into a list from the form data dict
        to_predict_list = list(form_data.values())

        # Ensure all values are integers
        to_predict_list = list(map(int, to_predict_list))

        # Log
        logger.debug(f"Received input for prediction: {to_predict_list}")

        # Run data through Decision Tree model
        results = value_predictor(to_predict_list)

        # If the result is a 1
        if int(results) == 1:
            prediction = "**Income more than 50K**"

        # If the result is a 0
        else:
            prediction = "**Income less than 50K**"

        # Log
        logger.debug(f'Prediction result: {prediction}')

        # Log
        logger.debug('Results rendered ...')

        # Render the model.html template with results
        return render_template('model.html', prediction=prediction, model_page_data=model_page_data)

    # Log
    logger.debug('Rendered model.html for GET request, no other return statement activated ...')
    # If not a POST request, or if no other return has been executed, render the model.html for GET request
    return render_template('model.html', model_page_data=model_page_data)


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    # Log
    logger.debug("contact_page() accessed ...")

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

            # Log
            logger.debug('Form data grabbed ...')

            # Insert data into ContactSubmissions table
            new_contact_submission = ContactSubmissions(email=sender, name=name, subject=subject, message=message)
            db.session.add(new_contact_submission)
            db.session.commit()

            # Log
            logger.debug("Form data added to database ...")

            # Create EmailMessage object
            msg = EmailMessage()
            msg['From'] = getenv("EMAIL_USERNAME")  # Use your authenticated email address
            msg['Reply-To'] = sender
            msg['To'] = getenv("EMAIL_USERNAME")  # Destination email
            msg['Subject'] = subject

            # Set the content of the email
            msg.set_content(f'Name: {name} <{sender}>\n\n{message}')

            # Send the email
            with SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(getenv("EMAIL_USERNAME"), getenv('WEB_APP_SECRET'))
                server.sendmail(getenv("EMAIL_USERNAME"), getenv("EMAIL_USERNAME"), msg.as_string())
                logger.debug(".sendmail() was activated")
                server.quit()
                logger.debug("context handler: below")

            # Set message to be displayed when email is sent successfully
            flash('Your message has been sent successfully.', 'success')

            return redirect(url_for('contact_page'))

        except SMTPAuthenticationError as e:

            # Set message to be displayed when email is not successfully sent
            flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('contact_page'))

    return render_template('contact.html')

# For deployment use
# @app.route('/health')
# def health():
#     return 200, 'OK'


if __name__ == '__main__':
    # Create a logger object
    logger = getLogger('web.application.logger')

    # Set the level of the logger object
    logger.setLevel(DEBUG)

    # Create the formatter object
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a rotating file handler object
    log_handler = RotatingFileHandler(
        './logs/flask/error.log',
        maxBytes=75 * 1000,
        backupCount=5
    )

    # Set the formatter for the rotating file handler object
    log_handler.setFormatter(formatter)

    # Set the level of the rotating file handler object
    log_handler.setLevel(DEBUG)

    # Add the rotating file handler object to the logger object
    logger.addHandler(log_handler)

    # Log that main() is accessed
    logger.debug('main() accessed ...')

    # Run development server
    app.run(debug=True, port=5000)
