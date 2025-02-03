import json
import os
import random
import string
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class AccountSettings:
    AUTH_TOKEN: str
    SHOULD_REFRESH_SESSION: bool = True
    FARM_ID: str | None = None
    CLIENT_VERSION: str = "2025-01-31T05:13"
    ACCOUNT_ID: str | None = None
    SESSION_ID: str | None = None
    TRANSACTION_ID: str = "undefined"
    DEVICE_TRACKER_ID: str | None = None
    LOGGED_IN_AT: datetime | None = None

    _session_data: dict | None = None

    def __init__(self, **kwargs):
        self.AUTH_TOKEN = os.getenv("AUTH_TOKEN")
        self.SHOULD_REFRESH_SESSION = os.getenv("SHOULD_REFRESH_SESSION", True)
        self._session_data = self.get_session_data()

    def get_session_data(self) -> dict:
        session_file = self.get_session_file()
        session_file_exists = False
        if session_file.exists():
            session_file_exists = True

        if self._session_data is None:
            if self.SHOULD_REFRESH_SESSION or not session_file_exists:
                self.update_session_data()
            else:
                self._session_data = self.get_session_file_data()
        return self._session_data

    def update_session_data(self):
        session_file = self.get_session_file()
        if session_file.exists():
            session_response = self._request_session()
            self._session_data = session_response
            session_file.write_text(json.dumps(session_response, indent=4), encoding="utf-8")
        self._init_variables()

    @staticmethod
    def generate_random_id_for_session():
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=9))

    @staticmethod
    def get_session_file() -> Path:
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        return config_dir / "session.json"

    @staticmethod
    def get_session_file_data() -> dict | None:
        session_file = AccountSettings.get_session_file()

        if not session_file.exists():
            return None

        with session_file.open("r", encoding="utf-8") as f:
            session_data = json.load(f)
        return session_data

    def _init_variables(self):
        self.ACCOUNT_ID = self._session_data['linkedWallet']
        self.FARM_ID = self._session_data['farmId']
        self.SESSION_ID = self._session_data['sessionId']
        self.DEVICE_TRACKER_ID = self._session_data['deviceTrackerId']
        self.LOGGED_IN_AT = datetime.fromisoformat(self._session_data['startedAt'].rstrip("Z"))

    def _request_session(self) -> dict:
        response = requests.post(
            "https://api.sunflower-land.com/session",
            json={"clientVersion": self.CLIENT_VERSION},
            headers={
                "content-type": "application/json;charset=UTF-8",
                "Authorization": f"Bearer {self.AUTH_TOKEN}",
                "X-Fingerprint": "X",
                "X-Transaction-ID": self.generate_random_id_for_session(),
            }
        )

        if response.status_code == 503:
            # Handle server maintenance or throttling
            data = response.json()
            if data.get("message") == "Temporary maintenance":
                raise Exception("Server is under maintenance.")
            raise Exception("Session server error.")
        elif response.status_code == 429:
            raise Exception("Too many requests. Try again later.")
        elif response.status_code == 401:
            raise Exception("Session expired. Please log in again.")
        elif response.status_code >= 400:
            raise Exception(f"Session error: {response.status_code} - {response.text}")

        return response.json()


account_settings = AccountSettings()
