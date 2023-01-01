from api_key import API_KEY

BASE_PATH = "https://api.apilayer.com/fixer/latest?"
API_KEY = API_KEY

rules = {
    "archive": True,
    "email": {
        "enable": True,
        "preferred": ["USD", "IRR", "EUR", "BTC", "EUR"]
    }
}
