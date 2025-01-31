import base64
import json
import random
import time
import uuid
from datetime import datetime, timedelta

import pytz
import requests

from settings.account_settings import account_settings
from utils.consts import (
    API_URL,
)


def generate_device_tracker_id():
    """Generate a unique deviceTrackerId."""

    def load_session(token, transaction_id, retries=0):
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Transaction-ID": transaction_id,
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        }

        payload = {
            "clientVersion": account_settings.CLIENT_VERSION,
        }

        response = requests.post(f"{API_URL}/session", json=payload, headers=headers)

        if response.status_code == 503:
            # Handle server maintenance or throttling
            data = response.json()
            if data.get("message") == "Temporary maintenance":
                raise Exception("Server is under maintenance.")

            backoff = min(1000 * (2 ** retries), 10000)  # Exponential backoff
            jitter = random.uniform(0, 1000)
            time.sleep((backoff + jitter) / 1000)

            if retries < 3:
                return load_session(token, transaction_id, retries + 1)

            raise Exception("Session server error after retries.")

        if response.status_code == 429:
            raise Exception("Too many requests. Try again later.")

        if response.status_code == 401:
            raise Exception("Session expired. Please log in again.")

        if response.status_code >= 400:
            raise Exception(f"Session error: {response.status_code} - {response.text}")

        data = response.json()
        return data.get("deviceTrackerId")

    return load_session(account_settings.AUTH_TOKEN, account_settings.TRANSACTION_ID)


def generate_time_for_planting():
    def get_time(milliseconds_delta=0):
        kyiv_tz = pytz.timezone("Europe/Kyiv")
        kyiv_time = datetime.now(kyiv_tz) + timedelta(milliseconds=milliseconds_delta)
        utc_time = kyiv_time.astimezone(pytz.utc)
        return utc_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    random_milliseconds = random.randint(0, 10000)
    return get_time(random_milliseconds)


def generate_unique_crop_id():
    return str(uuid.uuid4()).replace("-", "")[:8]


def generate_cached_key():
    """Generates a Base64-encoded JSON cache key with the current timestamp."""
    farm_session = {
        # Subtract 30 seconds in milliseconds
        "loggedInAt": int(time.time() * 1000) - (30 * 1000),
        # "farmId": FARM_ID,
        # "loggedInAt": int(time.time() * 1000),
        # "account": account_id,
    }
    cache_key = base64.b64encode(json.dumps(farm_session).encode()).decode()
    return cache_key
