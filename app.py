from flask import Flask, request, jsonify
from flask_mail import Mail
from celery_app import make_celery, send_email_task
import os

app = Flask(__name__)

# Mail config
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME")
)

mail = Mail(app)
celery = make_celery(app)

@app.route("/add-book", methods=["POST"])
def add_book():
    title = request.json.get("title")
    user_email = request.json.get("email")

    send_email_task.delay(
        user_email,
        "Libro agregado",
        f"El libro '{title}' fue agregado correctamente."
    )

    return jsonify({"message": "Libro agregado y correo en cola"}), 201

@app.route("/delete-book", methods=["POST"])
def delete_book():
    title = request.json.get("title")
    user_email = request.json.get("email")

    send_email_task.delay(
        user_email,
        "Libro eliminado",
        f"El libro '{title}' fue eliminado correctamente."
    )

    return jsonify({"message": "Libro eliminado y correo en cola"}), 200

if __name__ == "__main__":
    app.run(debug=True)