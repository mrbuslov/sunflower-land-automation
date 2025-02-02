import json
import random
import string
import time
from datetime import datetime
from pathlib import Path

import requests
from pydantic_settings import BaseSettings

_session_data = None


class AccountSettings(BaseSettings):
    AUTH_TOKEN: str
    SHOULD_REFRESH_SESSION: bool = True
    FARM_ID: str | None = None
    CLIENT_VERSION: str = "2025-01-31T05:13"
    ACCOUNT_ID: str | None = None
    SESSION_ID: str | None = None
    TRANSACTION_ID: str = "undefined"
    DEVICE_TRACKER_ID: str | None = None
    LOGGED_IN_AT: datetime | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        session_data = self.get_session_data()

        self.ACCOUNT_ID = session_data['linkedWallet']
        self.FARM_ID = session_data['farmId']
        self.SESSION_ID = session_data['sessionId']
        self.DEVICE_TRACKER_ID = session_data['deviceTrackerId']
        self.LOGGED_IN_AT = datetime.fromisoformat(session_data['startedAt'].rstrip("Z"))

    def get_session_data(self, force_update_session: bool = False) -> dict:
        global _session_data
        if _session_data is None or force_update_session is True:
            session_file = self.get_session_file()
            session_file_exists = False
            if session_file.exists():
                session_file_exists = True

            if force_update_session is True or self.SHOULD_REFRESH_SESSION or not session_file_exists:
                session_response = self._request_session()
                _session_data = session_response
                session_file.write_text(json.dumps(session_response, indent=4), encoding="utf-8")
            else:
                _session_data = self.get_session_file_data()
        return _session_data

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

    class Config:
        env_file = ".env"
        frozen = False
        populate_by_name = True


account_settings = AccountSettings()
