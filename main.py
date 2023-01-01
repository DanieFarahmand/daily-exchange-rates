import json

import requests

from config import BASE_PATH, API_KEY, rules


def get_rates():
    response = requests.get(BASE_PATH, API_KEY)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def archive(timestamp, rates):
    with open(f"archive/{timestamp}.json", "w") as f:
        f.write(json.dumps(rates))


if __name__ == "__main__":
    res = get_rates()

    if rules["archive"]:
        archive(res["timestamp"], res["rates"])
