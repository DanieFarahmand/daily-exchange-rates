import json
from datetime import datetime

import requests
from khayyam import JalaliDatetime

from config import url, rules
from mail import send_smtp_email
from notification import send_sms


def get_rates():
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def archive(file_name, rates):
    with open(f"archive/{file_name}.json", "w") as f:
        f.write(json.dumps(rates))


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


def check_notify_rules(rates):
    preferred = rules["notification"]["preferred"]
    msg = ""
    for exc in preferred.keys():

        if rates[exc] >= preferred[exc]["max"]:
            msg += f"{exc} reached {rates[exc]} passed max: {preferred[exc]['max']} "

        if rates[exc] <= preferred[exc]["min"]:
            msg += f"{exc} reached {rates[exc]} passed min: {preferred[exc]['min']} "

    return msg


def send_notification(msg):
    datetime_now = JalaliDatetime(datetime.now()).strftime(" %A %Y-%m-%d %H:%M")
    msg += datetime_now
    print(msg)
    send_sms(msg)


if __name__ == "__main__":
    res = get_rates()

    if rules["archive"]:
        archive(file_name=res['timestamp'], rates=res["rates"])

    if rules["email"]["enable"]:
        send_mail(res['timestamp'], res["rates"])

    if rules["notification"]["enable"]:
        notification_msg = check_notify_rules(res["rates"])

        if notification_msg:
            send_notification(notification_msg)
