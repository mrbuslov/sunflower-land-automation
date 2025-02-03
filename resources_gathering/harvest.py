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
    generate_cached_key, set_new_hole_last_harvested_at, arg_parser_harvest,
    split_payloads_by_created_at,
)


@handle_gathering_errors
def harvest(crop_name: str = None):
    """
    Harvests all crops in land holes.
    If crop_name is specified, the harvesting time will be calculated (so you can plant and harvest again)
    """
    print('Starting harvesting  ...')
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
    ]
    if not to_harvest:
        print('Nothing to harvest')
        return
    if crop_name is not None:
        to_harvest = to_harvest[:resources_settings.CROPS_AMOUNT[crop_name]]

    payload = {
        "sessionId": account_settings.SESSION_ID,
        "actions": to_harvest,
        "clientVersion": account_settings.CLIENT_VERSION,
        "cachedKey": cached_key,
        "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
    }
    for request_payload in split_payloads_by_created_at(payload):
        response = requests.post(ApiRouter.AUTOSAVE, headers=DEFAULT_HEADERS(), json=request_payload)
        print("Status code harvest:", response.status_code)

        # set them as available
        if response.status_code == 200:
            for action in to_harvest:
                resources_settings.LAND_HOLES_AVAILABILITY[action["index"]] = True
        else:
            print(response.text)
            return

    for harvest_operation in to_harvest:
        set_new_hole_last_harvested_at(harvest_operation["index"], harvest_operation["createdAt"])


if __name__ == "__main__":
    args = arg_parser_harvest()
    harvest(args.name)
