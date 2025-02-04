import asyncio
from datetime import timedelta

import requests

from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.consts import (
    DEFAULT_HEADERS,
)
from utils.decorators import handle_gathering_errors
from utils.schemas import ApiRouter
from utils.utils import (
    generate_time_for_gathering_operation,
    generate_unique_crop_id,
    generate_cached_key, arg_parser_plant, set_new_hole_last_planted_at,
    split_payloads_by_created_at,
)


@handle_gathering_errors
async def plant(
        name: str = None,
        amount: int = -1
):
    """
    Plants seeds in free land holes.
    If amount is -1, all seeds will be planted.
    NOTE: it plants seeds in past, so it can be easy to harvest
    """
    cached_key = generate_cached_key()
    if not resources_settings.is_able_to_plant(amount):
        print(f"Not enough land holes to plant {amount} {name}. Available: {sum(resources_settings.LAND_HOLES_AVAILABILITY.values())}")
        return
    elif not resources_settings.is_crops_amount_sufficient(name, amount):
        print(f"Not enough {name} to plant {amount}. Available: {resources_settings.CROPS_AMOUNT[name]}")
        return

    to_plant = [
        {
            "type": "seed.planted",
            "index": hole_index,
            "item": name,
            "cropId": generate_unique_crop_id(),
            "createdAt": generate_time_for_gathering_operation(start_time=None),  # calculate_planting_time(hole_index)
        }
        for hole_index in resources_settings.LAND_HOLES
        if resources_settings.LAND_HOLES_AVAILABILITY[hole_index]
    ]
    to_plant = to_plant[:amount] if amount != -1 else to_plant
    to_plant = to_plant[:resources_settings.CROPS_AMOUNT[name]]
    payload = {
        "sessionId": account_settings.SESSION_ID,
        "actions": to_plant,
        "clientVersion": account_settings.CLIENT_VERSION,
        "cachedKey": cached_key,
        "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
    }

    print(f'Starting planting {len(to_plant)}/{resources_settings.CROPS_AMOUNT[name]} {name}...')
    for request_payload in split_payloads_by_created_at(payload):
        response = requests.post(ApiRouter.AUTOSAVE, headers=DEFAULT_HEADERS(), json=request_payload)
        print("Status code plant:", response.status_code)
        response.raise_for_status()

        # set them as unavailable
        if response.status_code == 200:
            for action in to_plant:
                resources_settings.LAND_HOLES_AVAILABILITY[action["index"]] = False

    for plant_operation in to_plant:
        set_new_hole_last_planted_at(plant_operation["index"], plant_operation["createdAt"])
    resources_settings.CROPS_AMOUNT[name] -= len(to_plant)


if __name__ == "__main__":
    args = arg_parser_plant()
    asyncio.run(plant(args.name, args.amount))
