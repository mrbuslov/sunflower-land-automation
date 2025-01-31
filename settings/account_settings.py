import json
import random
import string
from pathlib import Path

import requests
from pydantic_settings import BaseSettings


# TODO: regenerate device tracker id if expired (generate_device_tracker_id)
class AccountSettings(BaseSettings):
    AUTH_TOKEN: str
    FARM_ID: str | None = None
    CLIENT_VERSION: str = "2025-01-31T05:13"
    ACCOUNT_ID: str | None = None
    SESSION_ID: str | None = None
    TRANSACTION_ID: str = "undefined"
    DEVICE_TRACKER_ID: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        session_file = self.get_session_file()

        if not session_file.exists():
            session_response = self._request_session()
            session_file.write_text(json.dumps(session_response, indent=4), encoding="utf-8")

        with session_file.open("r", encoding="utf-8") as f:
            session_data = json.load(f)

        self.ACCOUNT_ID = session_data['linkedWallet']
        self.FARM_ID = session_data['farmId']
        self.SESSION_ID = session_data['sessionId']
        self.DEVICE_TRACKER_ID = session_data['deviceTrackerId']

    def _request_session(self) -> dict:
        return requests.post(
            "https://api.sunflower-land.com/session",
            json={"clientVersion": self.CLIENT_VERSION},
            headers={
                "content-type": "application/json;charset=UTF-8",
                "Authorization": f"Bearer {self.AUTH_TOKEN}",
                "X-Fingerprint": "X",
                "X-Transaction-ID": self.generate_random_id_for_session(),
            }
        ).json()

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


account_settings = AccountSettings()
