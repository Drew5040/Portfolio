import socket
from os import getenv
from email.message import EmailMessage
from smtplib import SMTP, SMTPException
from flask import current_app, flash
from celery import shared_task
from celery.utils.log import get_task_logger


@shared_task(name='send_email_task', queue='email', bind=True, rate_limit='10/m')
def send_email_task(self, sender, name, subject, message):
    # Initialize the Celery logger instance
    lager = get_task_logger(__name__)
    with current_app.app_context():
        try:
            # Create EmailMessage object
            msg = EmailMessage()
            msg['From'] = getenv("EMAIL_USERNAME")
            msg['Reply-To'] = sender
            msg['To'] = getenv('EMAIL_USERNAME')
            msg['Subject'] = subject

            # Log the msg object was created
            lager.info("Message object created")

            # Set the content of the email
            msg.set_content(f'Name: {name} <{sender}>\n\n{message}')

            # Grab the local hostname for SMTP parameter
            local_hostname = socket.gethostname()
            lager.info('Attempting to use hostname: %s', local_hostname)

            # Send the email
            with SMTP("smtp.office365.com", 587, local_hostname=local_hostname) as server:
                server.starttls()
                lager.debug('TLS initiated...')
                server.login(getenv("EMAIL_USERNAME"), getenv('WEB_APP_SECRET'))
                lager.debug('Server login successful...')
                server.sendmail(getenv("EMAIL_USERNAME"), getenv("EMAIL_USERNAME"), msg.as_string())
                lager.debug("Email was sent ...")
                server.quit()

        except SMTPException as e:

            # Log if email is not successfully sent
            lager.error(f'SMTP error occurred: {str(e)}', 'error')

            # Retry sending after 5 mins
            self.retry(exc=e, countdown=30, max_retries=5)


@shared_task(name='other_task', bind=True, rate_limit='29/m')
def other_task():
    pass
