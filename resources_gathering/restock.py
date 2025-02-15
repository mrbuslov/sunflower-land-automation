import asyncio

from api.services import send_data
from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.decorators import handle_gathering_errors, wait_if_operation_performing
from utils.utils import (
    generate_time_for_gathering_operation,
    generate_cached_key,
)


@wait_if_operation_performing
@handle_gathering_errors
async def restock():
    """
    Restock crops 
    """
    cached_key = generate_cached_key()

    if not resources_settings.is_able_to_restock_shipment:
        print('Not able to restock now')
        return
    payload = {
        "sessionId": account_settings.SESSION_ID,
        "actions": [
            {
                "type": "shipment.restocked",
                "createdAt": generate_time_for_gathering_operation()
            }
        ],
        "clientVersion": account_settings.CLIENT_VERSION,
        "cachedKey": cached_key,
        "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
    }
    print('Starting restocking...')
    response = await send_data(payload)
    print("Status code restock:", response.status_code)


if __name__ == "__main__":
    asyncio.run(restock())
