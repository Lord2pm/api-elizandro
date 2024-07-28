from flask_mail import Mail, Message

# import os


mail = Mail()


def email_send(msg: str, recipients: str, subject: str):
    message = Message(
        subject=subject,
        recipients=[recipients],
        sender="luismuhele@gmail.com",
        # sender=os.getenv("MAIL_SENDER")
    )
    message.body = msg
    mail.send(message)
