import argparse
import base64
import json
import random
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Literal, Any

from settings.resources_settings import resources_settings
from utils.plants_schemas import PLANTS_DATA


def generate_time_for_gathering_operation(
        start_time: datetime | None = None,
        delta_seconds: int = 0,
        action: Literal['add', 'sub'] = 'add'
) -> str:
    if action == 'sub':
        delta_seconds = -delta_seconds
    date_time = start_time if start_time else datetime.utcnow()
    utc_time = date_time + timedelta(seconds=delta_seconds)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def generate_unique_crop_id():
    return str(uuid.uuid4()).replace("-", "")[:8]


def generate_cached_key():
    """Generates a Base64-encoded JSON cache key with the current timestamp."""
    farm_session = {
        # Subtract 30 seconds in milliseconds
        # "loggedInAt": int(time.time() * 1000) - (30 * 1000),
        "loggedInAt": 1738141191282,
        # "farmId": FARM_ID,
        # "loggedInAt": int(time.time() * 1000),
        # "account": account_id,
    }
    cache_key = base64.b64encode(json.dumps(farm_session).encode()).decode()
    return cache_key


def arg_parser_plant():
    parser = argparse.ArgumentParser(description="Plant resources")
    parser.add_argument(
        "name",
        type=str,
        nargs="?",
        default="Sunflower Seed",
        help="Name of resource to plant. Listed in utils/plants_schemas.py"
    )
    parser.add_argument(
        "amount",
        type=int,
        nargs="?",
        default=-1,
        help="Amount of resource to plant. -1 for all"
    )
    return parser.parse_args()


def arg_parser_harvest():
    parser = argparse.ArgumentParser(description="Harvest resources")
    parser.add_argument(
        "name",
        type=str,
        nargs="?",
        default="Sunflower Seed",
        help="Name of resource to plant. Listed in utils/plants_schemas.py"
    )
    return parser.parse_args()


def arg_parser_resources():
    parser = argparse.ArgumentParser(description="Gather resources")
    parser.add_argument(
        "amount",
        type=int,
        nargs="?",
        default=-1,
        help="Amount of resource to plant. -1 for all"
    )
    return parser.parse_args()



def divide_items_to_chunks(total: int, chunk: int) -> list[int]:
    result = [chunk] * (total // chunk)
    remainder = total % chunk
    if remainder:
        result.append(remainder)
    return result


def calculate_gathering_time(crop_name: str, hole_id: str) -> datetime:
    """Calculate gathering time for crop based on hole's harvested_at time and crop's growth time"""
    operations_data = resources_settings.get_holes_operations_data(hole_id)
    start_from_time = (
        operations_data['planted_at']
        if operations_data.get('planted_at')
        else operations_data['harvested_at']
    )
    return (
            start_from_time +
            timedelta(seconds=PLANTS_DATA[crop_name]["plantSeconds"]) +
            timedelta(seconds=random.randint(0, 10))
    )


def calculate_planting_time(hole_id: str) -> datetime:
    """Calculate gathering time for crop based on hole's harvested_at time and crop's growth time"""
    return resources_settings.get_holes_operations_data(hole_id)['harvested_at']


def set_new_hole_last_harvested_at(hole_id: str, new_created_at: str):
    new_created_at_datetime = datetime.fromisoformat(new_created_at.rstrip("Z"))
    resources_settings.OPERATIONS_INFO[hole_id]["harvested_at"] = new_created_at_datetime
    resources_settings.set_hole_operation_time(hole_id, {"harvested_at": new_created_at_datetime})


def set_new_hole_last_planted_at(hole_id: str, new_created_at: str):
    new_created_at_datetime = datetime.fromisoformat(new_created_at.rstrip("Z"))
    resources_settings.OPERATIONS_INFO[hole_id]["planted_at"] = new_created_at_datetime
    resources_settings.set_hole_operation_time(hole_id, {"planted_at": new_created_at_datetime})


def split_payloads_by_created_at(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Groups payloads by createdAt, bc gathering operations are sent as one request with same createdAt time"""
    actions = payload.get("actions", [])

    # Group actions by createdAt
    grouped_actions = defaultdict(list)
    for action in actions:
        created_at = action.get("createdAt")
        if created_at:
            grouped_actions[created_at].append(action)

    # Create separate payloads for each group
    split_payloads = []
    for created_at, grouped in grouped_actions.items():
        split_payloads.append({
            "sessionId": payload["sessionId"],
            "actions": grouped,
            "clientVersion": payload["clientVersion"],
            "cachedKey": payload["cachedKey"],
            "deviceTrackerId": payload["deviceTrackerId"],
        })

    return split_payloads

