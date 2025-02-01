import argparse
import base64
import json
import random
import time
import uuid
from datetime import datetime, timedelta

import pytz


def generate_time_for_planting():
    def get_time(milliseconds_delta=0):
        kyiv_tz = pytz.timezone("Europe/Kyiv")
        kyiv_time = datetime.now(kyiv_tz) + timedelta(milliseconds=milliseconds_delta)
        utc_time = kyiv_time.astimezone(pytz.utc)
        return utc_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    random_milliseconds = random.randint(0, 10000)
    return get_time(random_milliseconds)


def generate_unique_crop_id():
    return str(uuid.uuid4()).replace("-", "")[:8]


def generate_cached_key():
    """Generates a Base64-encoded JSON cache key with the current timestamp."""
    farm_session = {
        # Subtract 30 seconds in milliseconds
        "loggedInAt": int(time.time() * 1000) - (30 * 1000),
        # "farmId": FARM_ID,
        # "loggedInAt": int(time.time() * 1000),
        # "account": account_id,
    }
    cache_key = base64.b64encode(json.dumps(farm_session).encode()).decode()
    return cache_key


def arg_parser_plant():
    parser = argparse.ArgumentParser(description="Harvest resources")
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
