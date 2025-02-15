import asyncio
from datetime import datetime, timezone

from api.services import send_data
from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.decorators import handle_gathering_errors, wait_if_operation_performing
from utils.utils import (
    generate_time_for_gathering_operation,
    generate_cached_key, set_new_hole_last_harvested_at, arg_parser_harvest,
    split_payloads_by_created_at,
)


@wait_if_operation_performing
@handle_gathering_errors
async def harvest(crop_name: str = None):
    """
    Harvests all crops in land holes.
    If crop_name is specified, the harvesting time will be calculated (so you can plant and harvest again)
    """
    cached_key = generate_cached_key()

    to_harvest = [
        {
            "type": "crop.harvested",
            "index": hole_index,
            "createdAt": generate_time_for_gathering_operation(
                start_time=None  # calculate_gathering_time(crop_name, hole_index) if crop_name is not None else None
            ),
        }
        for hole_index in resources_settings.LAND_HOLES
        if not resources_settings.LAND_HOLES_AVAILABILITY[hole_index]
           and (
                   resources_settings.LAND_HOLES_DATA.get(hole_index, {}).get("next_planting_time", None)
                   and
                   datetime.now(timezone.utc) >= resources_settings.LAND_HOLES_DATA[hole_index]["next_planting_time"]
           )
    ]
    if not to_harvest:
        print('Nothing to harvest')
        return

    payload = {
        "sessionId": account_settings.SESSION_ID,
        "actions": to_harvest,
        "clientVersion": account_settings.CLIENT_VERSION,
        "cachedKey": cached_key,
        "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
    }

    print('Starting harvesting...')
    for request_payload in split_payloads_by_created_at(payload):
        response = await send_data(request_payload)
        print("Status code harvest:", response.status_code)

        # set them as available
        if response.status_code == 200:
            for action in to_harvest:
                resources_settings.LAND_HOLES_AVAILABILITY[action["index"]] = True

    for harvest_operation in to_harvest:
        set_new_hole_last_harvested_at(harvest_operation["index"], harvest_operation["createdAt"])
        resources_settings.LAND_HOLES_DATA[harvest_operation["index"]]["next_planting_time"] = datetime.now(timezone.utc)


if __name__ == "__main__":
    args = arg_parser_harvest()
    asyncio.run(harvest(args.name))
