import json
from datetime import datetime

from khayyam import JalaliDatetime

from config import rules
from fixer import get_rates
from mail import send_mail
from notification import send_sms


def archive(file_name, rates):
    with open(f"archive/{file_name}.json", "w") as f:
        f.write(json.dumps(rates))


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
