from settings.account_settings import account_settings

API_URL = "https://api.sunflower-land.com"

DEFAULT_HEADERS = lambda: {
    "content-type": "application/json;charset=UTF-8",
    "Authorization": f"Bearer {account_settings.AUTH_TOKEN}",
    "X-Fingerprint": "X",
    "X-Transaction-ID": account_settings.generate_random_id_for_session(),
}
