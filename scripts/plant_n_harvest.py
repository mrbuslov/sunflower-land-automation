import random
import asyncio
import traceback

from resources_gathering.harvest import harvest
from resources_gathering.plant import plant
from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.plants_schemas import PLANTS_DATA
from utils.utils import divide_items_to_chunks


async def plant_n_harvest(crop_name: str):
    """
    Plants seeds and harvests them.
    LEAVE THIS SCRIPT RUNNING IN THE BACKGROUND (NIGHT)
    """
    if crop_name not in resources_settings.CROPS_AMOUNT:
        print(f'ERROR: Crop {crop_name} not found in available plants')
        return

    print(f'Planting {resources_settings.CROPS_AMOUNT[crop_name]} {crop_name}')
    # divide by holes amount
    get_available_holes = lambda: [i for i in resources_settings.LAND_HOLES_AVAILABILITY.values() if i is True]
    available_holes = get_available_holes()
    while len(available_holes) == 0:
        print(f'Available holes for {crop_name} is 0. Waiting 10 seconds...')
        await asyncio.sleep(10)
        account_settings.update_session_data()
        await harvest()
        available_holes = get_available_holes()
    chunks_list = divide_items_to_chunks(
        resources_settings.CROPS_AMOUNT[crop_name],
        len(available_holes)
    )

    for chunk in chunks_list:
        print(f'Planting {chunk} {crop_name}')
        try:
            await plant(crop_name, chunk)
        except Exception as e:
            print(f"Couldn't plant crop {crop_name}. Error: {e}")
            traceback.print_exc()

        await asyncio.sleep(PLANTS_DATA[crop_name]["plantSeconds"] + random.randint(0, 10))
        account_settings.update_session_data()

        print(f'Harvesting {chunk} {crop_name}')
        try:
            await harvest(crop_name)
        except Exception as e:
            print(f"Couldn't harvest crop {crop_name}. Error: {e}")
            traceback.print_exc()
        print('-' * 80)


if __name__ == '__main__':
    PLANTS_CULTURES_SEEDS_TO_PLANT = [
        "Sunflower Seed",
        "Rhubarb Seed",
        "Carrot Seed",
        # "Potato Seed",
        # "Pumpkin Seed",
    ]
    for crop_name in PLANTS_CULTURES_SEEDS_TO_PLANT:
        asyncio.run(plant_n_harvest(crop_name))
