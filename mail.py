import json
import smtplib
from email.mime.text import MIMEText

from mail_config import receiver, username, password, sender


def send_smtp_email(body, subject):
    msg = MIMEText(body)
    msg['Subject'] = json.dumps(subject)
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(username, password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())

    print(msg)
