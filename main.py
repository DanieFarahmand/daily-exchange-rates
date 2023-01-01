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


def send_mail(subject, rates):
    exchanges = dict()
    if rules["email"]["preferred"] is not None:
        for exc in rules["email"]["preferred"]:
            exchanges[exc] = rates[exc]

    text = json.dumps(exchanges)
    send_smtp_email(text, subject)


if __name__ == "__main__":
    res = get_rates()

    if rules["archive"]:
        archive(res["timestamp"], res["rates"])

    if rules["email"]["enable"]:
        send_mail(res["timestamp"], res["rates"])
