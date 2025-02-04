import asyncio
from datetime import datetime, timezone

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
    generate_cached_key, split_payloads_by_created_at, arg_parser_resources,
)


@handle_gathering_errors
async def trees_cut_down(
        amount: int = -1
):
    """
    Cuts down available trees.
    If amount is -1, all trees will be cut.
    """
    cached_key = generate_cached_key()
    to_cut = [
        {
            "type": "timber.chopped",
            "index": tree_index,
            "item": "Axe",
            "createdAt": generate_time_for_gathering_operation(),
        }
        for tree_index, tree_data in resources_settings.TREES_DATA.items()
        if datetime.now(timezone.utc) >= tree_data['next_chop_time']
    ]
    to_cut = to_cut[:amount] if amount != -1 else to_cut
    to_cut = to_cut[:resources_settings.TOOLS_AMOUNT["Axe"]]
    payload = {
        "sessionId": account_settings.SESSION_ID,
        "actions": to_cut,
        "clientVersion": account_settings.CLIENT_VERSION,
        "cachedKey": cached_key,
        "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
    }

    if len(to_cut) == 0:
        print('Nothing to cut')
        return

    print(f'Starting cropping {len(to_cut)}/{len(resources_settings.TREES_DATA)} trees...')
    for request_payload in split_payloads_by_created_at(payload):
        response = requests.post(ApiRouter.AUTOSAVE, headers=DEFAULT_HEADERS(), json=request_payload)
        print("Status code trees cut:", response.status_code)
        response.raise_for_status()

        # update last cut time
        for action in to_cut:
            resources_settings.TREES_DATA[action["index"]]["next_chop_time"] = datetime.utcnow()
        resources_settings.TOOLS_AMOUNT["Axe"] -= len(to_cut)


if __name__ == '__main__':
    args = arg_parser_resources()
    asyncio.run(trees_cut_down(args.amount))
