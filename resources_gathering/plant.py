import requests

from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.consts import (
    DEFAULT_HEADERS,
)
from utils.schemas import ApiRouter
from utils.utils import (
    generate_time_for_planting,
    generate_unique_crop_id,
    generate_cached_key, arg_parser_plant,
)


def plant(
    name: str = None,
    amount: int = -1
):
    print('Starting planting...')
    if not resources_settings.is_able_to_plant(amount):
        print(f"Not enough land holes to plant {amount} {name}. Available: {sum(resources_settings.LAND_HOLES_AVAILABILITY.values())}")
        return
    elif not resources_settings.is_crops_amount_sufficient(name, amount):
        print(f"Not enough {name} to plant {amount}. Available: {resources_settings.CROPS_AMOUNT[name]}")
        return

    time_for_planting = generate_time_for_planting()
    cached_key = generate_cached_key()

    to_plant = [
        {
            "type": "seed.planted",
            "index": hole_index,
            "item": name,
            "cropId": generate_unique_crop_id(),
            "createdAt": time_for_planting,
        }
        for hole_index in resources_settings.LAND_HOLES
        if resources_settings.LAND_HOLES_AVAILABILITY[hole_index]
    ]
    to_plant = to_plant[:amount] if amount != -1 else to_plant
    payload = {
        "sessionId": account_settings.SESSION_ID,
        "actions": to_plant,
        "clientVersion": account_settings.CLIENT_VERSION,
        "cachedKey": cached_key,
        "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
    }
    response = requests.post(ApiRouter.AUTOSAVE, headers=DEFAULT_HEADERS(), json=payload)
    print("Status code plant:", response.status_code)

    # set them as unavailable
    if response.status_code == 200:
        for action in to_plant:
            resources_settings.LAND_HOLES_AVAILABILITY[action["index"]] = False
    else:
        print(response.text)


if __name__ == "__main__":
    args = arg_parser_plant()
    plant(args.name, args.amount)
