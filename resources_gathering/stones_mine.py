import asyncio
from datetime import datetime, timezone

import requests

from api.services import send_data
from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.consts import (
    DEFAULT_HEADERS,
)
from utils.decorators import handle_gathering_errors, wait_if_operation_performing
from utils.schemas import ApiRouter
from utils.utils import (
    generate_time_for_gathering_operation,
    generate_cached_key, split_payloads_by_created_at, arg_parser_resources,
)


@wait_if_operation_performing
@handle_gathering_errors
async def stones_plain_mine(
        amount: int = -1
):
    """
    Mines available stones.
    If amount is -1, all stones will be mined.
    """
    cached_key = generate_cached_key()
    to_mine = [
        {
            "type": "stoneRock.mined",
            "index": stone_index,
            "createdAt": generate_time_for_gathering_operation(),
        }
        for stone_index, stone_data in resources_settings.STONES_DATA.items()
        if datetime.now(timezone.utc) >= stone_data['next_mine_time']
    ]
    to_mine = to_mine[:amount] if amount != -1 else to_mine
    to_mine = to_mine[:resources_settings.TOOLS_AMOUNT["Pickaxe"]]
    payload = {
        "sessionId": account_settings.SESSION_ID,
        "actions": to_mine,
        "clientVersion": account_settings.CLIENT_VERSION,
        "cachedKey": cached_key,
        "deviceTrackerId": account_settings.DEVICE_TRACKER_ID,
    }

    if len(to_mine) == 0:
        print('Nothing to mine')
        return

    print(f'Starting mining {len(to_mine)}/{len(resources_settings.STONES_DATA)} stones...')
    for request_payload in split_payloads_by_created_at(payload):
        response = await send_data(request_payload)
        print("Status code stones mine:", response.status_code)

        # update last mine time
        for action in to_mine:
            resources_settings.STONES_DATA[action["index"]]["next_mine_time"] = datetime.now(timezone.utc)
        resources_settings.TOOLS_AMOUNT["Pickaxe"] -= len(to_mine)


if __name__ == '__main__':
    args = arg_parser_resources()
    asyncio.run(stones_plain_mine(args.amount))
