import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal
from settings.account_settings import AccountSettings

from utils.plants_schemas import PLANTS_DATA


class ResourcesSettings:
    LAND_HOLES: list[str] = []
    TREES: list[str] = []
    STONES: list[str] = []
    IRON_STONES: list[str] = []
    GOLD_STONES: list[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_variables()

    def init_variables(self):
        session_data = AccountSettings.get_session_file_data()

        self.RESOURCES_WAITING_TIME = {
            "tree": 60 * 60 * 2,
            "stone": 60 * 60 * 4,
        }

        self.LAND_HOLES = list(session_data['farm']['crops'].keys())
        self.LAND_HOLES_AVAILABILITY = {
            hole: not bool(session_data['farm']['crops'][hole].get('crop', False))
            for hole in self.LAND_HOLES
        }
        self.LAND_HOLES_DATA = {
            key: {
                "planted_at": (
                    self.from_timestamp(value.get('crop', {})["plantedAt"]) if value.get('crop', {}).get(
                        'plantedAt') else None
                ),
                "next_planting_time": (
                    self.from_timestamp(value.get('crop', {})["plantedAt"]) + timedelta(
                        seconds=PLANTS_DATA[value.get('crop', {})['name'] + " Seed"]['plantSeconds'])
                    if value.get('crop', {}).get('plantedAt') else datetime.now(timezone.utc)
                ),
            }
            for key, value in session_data['farm']['crops'].items()
        }

        self.TREES = list(session_data['farm']['trees'].keys())
        self.TREES_DATA: dict[str, dict[str, datetime]] = {
            key: {
                "chopped_at": self.from_timestamp(value['wood']["choppedAt"]),
                "next_chop_time": self.from_timestamp(value['wood']["choppedAt"]) + timedelta(
                    seconds=self.RESOURCES_WAITING_TIME["tree"]),
            }
            for key, value in session_data['farm']['trees'].items()
        }

        self.STONES = list(session_data['farm']['stones'].keys())
        self.STONES_DATA: dict[str, dict[str, datetime]] = {
            key: {
                "mined_at": self.from_timestamp(value['stone']["minedAt"]),
                "next_mine_time": self.from_timestamp(value['stone']["minedAt"]) + timedelta(
                    seconds=self.RESOURCES_WAITING_TIME["stone"]),
            }
            for key, value in session_data['farm']['stones'].items()
        }

        self.IRON_STONES = list(session_data['farm']['iron'].keys())
        self.GOLD_STONES = list(session_data['farm']['gold'].keys())

        self.CROPS_AMOUNT = {
            key: int(float(value))
            for key, value in session_data['farm']["inventory"].items()
            if key in PLANTS_DATA
        }
        self.TOOLS_AMOUNT: dict[str, int] = {
            "Axe": (
                int(session_data['farm']['inventory']['Axe'])
                if session_data['farm']['inventory'].get('Axe')
                else 0
            ),
            "Pickaxe": (
                int(session_data['farm']['inventory']['Pickaxe'])
                if session_data['farm']['inventory'].get('Pickaxe')
                else 0
            ),
        }

        self.LAST_RESTOCKED_AT = self.from_timestamp(session_data['farm']['shipments']['restockedAt'])
        self.NEXT_RESTOCK_TIME = self.LAST_RESTOCKED_AT + timedelta(hours=17)

        self.OPERATIONS_CONFIG_DIR = Path("config")
        self.OPERATIONS_CONFIG_FILE = self.OPERATIONS_CONFIG_DIR / "crops_operations.json"
        self.OPERATIONS_INFO = self.get_holes_operations_data()

    def is_able_to_plant(self, amount: int) -> bool:
        """Check if there are enough land holes to plant"""
        if amount == -1:
            return sum(self.LAND_HOLES_AVAILABILITY.values()) > 0
        return sum(self.LAND_HOLES_AVAILABILITY.values()) >= amount

    def is_crops_amount_sufficient(self, name: str, amount: int) -> bool:
        """Check if crops amount is sufficient"""
        if amount == -1:
            return int(self.CROPS_AMOUNT[name]) > 0
        return self.CROPS_AMOUNT[name] >= amount

    # TODO: implement https://stackoverflow.com/questions/8793448/how-to-convert-to-a-python-datetime-object-with-json-loads
    def get_holes_operations_data(self, hole_index: str = None) -> dict | datetime:
        """
        Reads the last planted times from the JSON config file.

        If hole_index is provided, return only the value for that hole.
        If the file does not exist, initialize it first.
        """
        data = self._get_crops_operations()['land_holes']
        data = {
            key: {
                "planted_at": (
                    datetime.fromisoformat(value_dict['planted_at'])
                    if isinstance(value_dict['planted_at'], str) else value_dict['planted_at']
                ),
                "harvested_at": (
                    datetime.fromisoformat(value_dict['harvested_at'])
                    if isinstance(value_dict['harvested_at'], str) else value_dict['harvested_at']
                )
            }
            for key, value_dict in data.items()
        }
        if hole_index is None:
            return data  # Return the whole dictionary
        elif hole_index in data:
            return data[hole_index]  # Return specific hole timestamp
        else:
            raise ValueError(f"Hole '{hole_index}' is not in the LAND_HOLES list. (get_holes_operations_data)")

    def set_hole_operation_time(
            self,
            hole_index: str,
            planting_data: dict[Literal['planted_at', 'harvested_at'], datetime]
    ):
        """Updates the planting time of a specific hole in the JSON config file."""
        data = self._get_crops_operations()
        holes_data = self._get_crops_operations()['land_holes']
        if hole_index not in holes_data:
            raise ValueError(f"Hole '{hole_index}' is not in the LAND_HOLES list. (set_hole_operation_time)")

        holes_data[hole_index] |= planting_data
        holes_data = {
            key: {
                "planted_at": value['planted_at'].isoformat() if isinstance(value['planted_at'], datetime) else value[
                    'planted_at'],
                "harvested_at": value['harvested_at'].isoformat() if isinstance(value['harvested_at'], datetime) else
                value['harvested_at']
            }
            for key, value in holes_data.items()
        }
        data['land_holes'] = holes_data
        with open(self.OPERATIONS_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def from_timestamp(self, timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

    def on_account_settings_update(self):
        self.init_variables()

    def _set_holes_default_operation_data(self):
        """Creates or updates the JSON config file with the current timestamp."""
        self.OPERATIONS_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            hole: {
                "planted_at": None,
                "harvested_at": datetime.utcnow().isoformat(),
            }
            for hole in self.LAND_HOLES
        }

        data = {"land_holes": data}
        with open(self.OPERATIONS_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return data

    def _get_crops_operations(self):
        if not self.OPERATIONS_CONFIG_FILE.exists():
            print('No operations config file found. Creating one...')
            data = self._set_holes_default_operation_data()
        else:
            with open(self.OPERATIONS_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        return data

    @property
    def is_able_to_restock_shipment(self) -> bool:
        return datetime.now(timezone.utc) >= self.NEXT_RESTOCK_TIME


resources_settings = ResourcesSettings()
