from os import getenv
from logging import debug, info
from json import dumps
from flask import Blueprint, redirect, url_for
from flask import request, render_template, flash
from helper import value_predictor, validate_form_entries
from email.message import EmailMessage
from smtplib import SMTPAuthenticationError, SMTP


# Create a Blueprint instance
app = Blueprint('navigation', __name__)


# Set homepage route
@app.route('/')
def home_page():
    return render_template('welcome.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/model')
def model_page():
    return render_template('model.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    debug("contact page accessed")
    if request.method == 'POST':
        debug("POST if block accessed")
        # Grab form data
        sender = request.form['email']
        name = request.form['name']
        subject = request.form['subject']
        message = request.form['message']
        debug("Form data grabbed, also right above try-block")

        try:
            debug("Try-block accessed")
            # Validate form data
            if not sender or not name or not subject or not message:
                raise ValueError("All fields are required")
            debug(f"Sender: {sender}")
            debug(f"Name: {name}")
            debug(f"Subject: {subject}")
            debug(f"Message: {message}")

            # Create EmailMessage object
            msg = EmailMessage()
            msg['From'] = getenv("EMAIL_USERNAME")  # Use your authenticated email address
            msg['Reply-To'] = sender
            msg['To'] = getenv("EMAIL_USERNAME")  # Destination email
            msg['Subject'] = subject
            msg.set_content(f'Name: {name} <{sender}>\n\n{message}')

            # Log msg values
            debug("below message content")
            debug("Message values:")
            for key, value in msg.items():
                debug(f"{key}: {value}")

            # Send the email
            with SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(getenv("EMAIL_USERNAME"), getenv('WEB_APP_SECRET'))
                server.sendmail(getenv("EMAIL_USERNAME"), getenv("EMAIL_USERNAME"), msg.as_string())
                debug(".sendmail() was activated")
                server.quit()
                debug("context handler: below")

            flash('Your message has been sent successfully.', 'success')
            debug("above first 'url_for()'")
            return redirect(url_for('navigation.contact_page'))  # Redirect to prevent form resubmission on page refresh
        except SMTPAuthenticationError as e:
            flash(f'An error occurred: {str(e)}', 'error')
            debug("above second 'url_for()'")
            return redirect(url_for('navigation.contact_page'))  # Redirect even if there's an error

    return render_template('contact.html')


# Display prediction
@app.route('/model', methods=['POST'])
def result():
    info('result page accessed...')

    if request.method == 'POST':

        form_data = request.form.to_dict()
        boole, errors, form_data = validate_form_entries(form_data)

        if not boole:
            errors_json = dumps(errors)
            print("errors_json: ", errors_json)
        else:
            errors_json = dumps({})

        if boole:
            to_predict_list = list(form_data.values())
            print(to_predict_list)
            to_predict_list = list(map(int, to_predict_list))
            print(to_predict_list)
            debug(f"Received input for prediction: {to_predict_list}")

            results = value_predictor(to_predict_list)

            if int(results) == 1:
                prediction = "**Income more than 50K**"
            else:
                prediction = "**Income less than 50K**"

            debug(f'Prediction result: {prediction}')

            return render_template('model.html', prediction=prediction)

        else:
            debug('error_message accessed...')
            form_data = request.form.to_dict()
            print('form_data that gets passed to error in entry template: ', form_data)
            print('errors json fields: ', errors_json)
            return render_template('model.html',
                                   form_data=form_data,
                                   errors_json=errors_json,
                                   error_message='**Please fill out all required fields**')

# @app.route('/health')
# def health():
#     return 200, 'OK'
