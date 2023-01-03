import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import requests
from khayyam import JalaliDatetime

from config import rules
from .mail_config import receiver, username, password, sender


def send_api_email(subject, body):
    return requests.post(
        "https://api.mailgun.net/v3/inprobes/messages",
        auth=("api", "n"),
        data={
            "from": "Hosein finance@inprobes.com",
            "to": ["hs.ramezanpoor@gmail.com", "hosein@inprobes.com"],
            "subject": subject,
            "text": body
        }
    )


def send_smtp_email(body, subject):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(username, password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())

        print(msg)


def send_mail(timestamp, rates):
    datetime_now = JalaliDatetime(datetime.now()).strftime(" %A %Y-%m-%d %H:%M")
    subject = f"{timestamp} {datetime_now} rates"

    if rules["email"]["preferred"] is not None:
        tmp = dict()
        for exc in rules["email"]["preferred"]:
            tmp[exc] = rates[exc]
        rates = tmp

    text = f"{rates}"

    send_smtp_email(subject, text)
