import random
import time

from resources_gathering.harvest import harvest
from resources_gathering.plant import plant
from settings.resources_settings import resources_settings
from utils.plants_schemas import PLANTS_DATA
from utils.utils import divide_items_to_chunks, arg_parser_harvest


def plant_n_harvest(crop_name: str):
    """
    Plants seeds and harvests them.
    LEAVE THIS SCRIPT RUNNING IN THE BACKGROUND (NIGHT)
    """
    print(f'Planting {resources_settings.CROPS_AMOUNT[crop_name]} {crop_name}')
    # divide by holes amount
    chunks_list = divide_items_to_chunks(
        resources_settings.CROPS_AMOUNT[crop_name],
        len(resources_settings.LAND_HOLES)
    )

    for chunk in chunks_list:
        print(f'Planting {chunk} {crop_name}')
        try:
            plant(crop_name, chunk)
        except Exception as e:
            print(f'Couldn\'t plant crop {crop_name}. Error: {e}')

        time.sleep(PLANTS_DATA[crop_name]["plantSeconds"] + random.randint(0, 10))

        print(f'Harvesting {chunk} {crop_name}')
        try:
            harvest(crop_name)
        except Exception as e:
            print(f'Couldn\'t harvest crop {crop_name}. Error: {e}')
        print('-' * 80)


if __name__ == '__main__':
    PLANTS_CULTURES_SEEDS_TO_PLANT = [
        "Sunflower Seed",
        # "Potato Seed",
        # "Pumpkin Seed",
    ]
    for crop_name in PLANTS_CULTURES_SEEDS_TO_PLANT:
        plant_n_harvest(crop_name)
