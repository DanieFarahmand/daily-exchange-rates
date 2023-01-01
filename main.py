import json

import requests

from config import BASE_PATH, API_KEY, rules
from mail import send_smtp_email


def get_rates():
    response = requests.get(BASE_PATH, API_KEY)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def archive(timestamp, rates):
    with open(f"archive/{timestamp}.json", "w") as f:
        f.write(json.dumps(rates))


def send_mail(timestamp, rates):
    exchanges = dict()
    if rules["email"]["preferred"] is not None:
        for exc in rules["email"]["preferred"]:
            exchanges[exc] = rates[exc]

    text = json.dumps(exchanges)
    send_smtp_email(text, timestamp)


def send_notification(rates):
    preferred = rules["notification"]["preferred"]
    msg = ""
    for exc in preferred.keys():

        if rates[exc] >= preferred[exc]["max"]:
            msg += f"{exc} reached max: {rates[exc]} \n"

        if rates[exc] <= preferred[exc]["min"]:
            msg += f"{exc} reached min: {rates[exc]} \n"
    print(msg)


if __name__ == "__main__":
    res = get_rates()

    if rules["archive"]:
        archive(res["timestamp"], res["rates"])

    if rules["email"]["enable"]:
        send_mail(res["timestamp"], res["rates"])

    if rules["notification"]["enable"]:
        send_notification(res["rates"])
