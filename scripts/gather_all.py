import asyncio

from resources_gathering.trees_cut import trees_cut_down
from scripts.plant_n_harvest import plant_n_harvest
from settings.resources_settings import resources_settings


async def gather_all():
    """
    Gathers all crops + resources
    """

    async def _plant_n_harvest():
        PLANTS_CULTURES_SEEDS_TO_PLANT = [
            "Sunflower Seed",
            "Rhubarb Seed",
            "Carrot Seed",
            # "Potato Seed",
            # "Pumpkin Seed",
        ]
        for crop_name in PLANTS_CULTURES_SEEDS_TO_PLANT:
            await plant_n_harvest(crop_name)

    async def _cut_down_trees():
        while resources_settings.TOOLS_AMOUNT["Axe"] >= 0:
            await trees_cut_down()
            await asyncio.sleep(resources_settings.RESOURCES_WAITING_TIME['tree'])
        else:
            print('No more trees to cut')

    task1 = asyncio.create_task(_cut_down_trees())
    task2 = asyncio.create_task(_plant_n_harvest())
    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    asyncio.run(gather_all())
