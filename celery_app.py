from celery import Celery
from flask_mail import Message, Mail
from flask import Flask
import os

def make_celery(app: Flask):
    celery = Celery(
        app.import_name,
        broker=os.getenv("CELERY_BROKER_URL"),
        backend=os.getenv("CELERY_BROKER_URL")
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_mail(app):
    return Mail(app)

celery = Celery(__name__, broker=os.getenv("CELERY_BROKER_URL"))

@celery.task(name="send_email_task")
def send_email_task(to, subject, body):
    app = Flask(__name__)
    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME")
    )
    mail = Mail(app)
    with app.app_context():
        msg = Message(subject, recipients=[to], body=body)
        mail.send(msg)