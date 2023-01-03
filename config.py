from api_key import API_KEY

BASE_PATH = "https://api.apilayer.com/fixer/latest?"
API_KEY = API_KEY

url = BASE_PATH + API_KEY

rules = {
    "archive": True,
    "email": {
        "enable": True,
        "preferred": ["USD", "IRR", "EUR", "BTC", "EUR"]
    },
    "notification": {
        "enable": True,
        "preferred": {
            "USD": {"min": 1.03, "max": 1.08},
            "IRR": {"min": 44800, "max": 44900},
            "BTC": {"min": 6.46, "max": 6.48}}
    }
}
