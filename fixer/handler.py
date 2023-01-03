import json

import requests

from fixer.config import url


def get_rates():
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None
