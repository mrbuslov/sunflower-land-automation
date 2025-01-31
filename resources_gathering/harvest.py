import requests
from utils.consts import (
    DEFAULT_HEADERS,
)
from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.schemas import ApiRouter
from utils.utils import (
    generate_time_for_planting,
    generate_cached_key,
)


time_for_harvesting = generate_time_for_planting()
cached_key = generate_cached_key()

payload = {
    "sessionId": account_settings.SESSION_ID,
    "actions": [
        {
            "type": "crop.harvested",
            "index": hole_index,
            "createdAt": time_for_harvesting,
        }
        for hole_index in resources_settings.LAND_HOLES
    ],
    "clientVersion": account_settings.CLIENT_VERSION,
    "cachedKey": cached_key,
    "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
}
response = requests.post(ApiRouter.AUTOSAVE, headers=DEFAULT_HEADERS(), json=payload)
