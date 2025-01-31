from enum import StrEnum

from settings.account_settings import account_settings
from utils.consts import API_URL


class ApiRouter(StrEnum):
    AUTOSAVE = f"{API_URL}/autosave/{account_settings.FARM_ID}"
    SESSION = f"{API_URL}/session"
