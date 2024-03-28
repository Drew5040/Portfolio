"""
This module defines the routes and views for the Flask web application, including
rendering pages, handling form submissions, and sending emails.
"""

from os import getenv
from logging import debug, info
from json import dumps
from email.message import EmailMessage
from smtplib import SMTP, SMTPAuthenticationError
from flask import Blueprint, redirect, url_for, request, render_template, flash
from helper import value_predictor, validate_form_entries


# Create a Blueprint instance
app = Blueprint('navigation', __name__)


@app.route('/')
def home_page():
    """Render the home/welcome page."""
    return render_template('welcome.html')


@app.route('/about')
def about_page():
    """Render the about page."""
    return render_template('about.html')


@app.route('/model')
def model_page():
    """Render the model prediction page."""
    return render_template('model.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    """
    Render the contact page and handle sending email on form submission.
    """
    debug("contact page accessed")
    if request.method == 'POST':
        debug("POST if block accessed")
        sender = request.form['email']
        name = request.form['name']
        subject = request.form['subject']
        message = request.form['message']
        debug("Form data grabbed, also right above try-block")

        try:
            debug("Try-block accessed")
            if not sender or not name or not subject or not message:
                raise ValueError("All fields are required")

            msg = EmailMessage()
            msg['From'] = getenv("EMAIL_USERNAME")
            msg['Reply-To'] = sender
            msg['To'] = getenv("EMAIL_USERNAME")
            msg['Subject'] = subject
            msg.set_content(f'Name: {name} <{sender}>\n\n{message}')

            debug("below message content")
            debug("Message values:")
            for key, value in msg.items():
                debug(f"{key}: {value}")

            with SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(getenv("EMAIL_USERNAME"), getenv('WEB_APP_SECRET'))
                server.sendmail(getenv("EMAIL_USERNAME"), getenv("EMAIL_USERNAME"), msg.as_string())
                debug(".sendmail() was activated")

            flash('Your message has been sent successfully.', 'success')
            debug("above first 'url_for()'")
        except SMTPAuthenticationError as e:
            flash(f'An error occurred: {str(e)}', 'error')
            debug("SMTP error occurred")

        return redirect(url_for('navigation.contact_page'))

    return render_template('contact.html')


@app.route('/model', methods=['POST'])
def result():
    """
    Handle the POST request to predict the result based on model.
    """
    info('result page accessed...')
    form_data = request.form.to_dict()
    boole, errors, form_data = validate_form_entries(form_data)

    if not boole:
        errors_json = dumps(errors)
        print("errors_json: ", errors_json)
        form_data = request.form.to_dict()
        print('form_data that gets passed to error in entry template: ', form_data)
        return render_template('model.html', form_data=form_data, errors_json=errors_json,
                               error_message='**Please fill out all required fields**')

    to_predict_list = list(form_data.values())
    to_predict_list = list(map(int, to_predict_list))
    debug(f"Received input for prediction: {to_predict_list}")

    results = value_predictor(to_predict_list)

    prediction = "**Income more than 50K**" if int(results) == 1 else "**Income less than 50K**"
    debug(f'Prediction result: {prediction}')

    return render_template('model.html', prediction=prediction)


@app.route('/health')
def health():
    """Return health status of the application."""
    return 'OK', 200
