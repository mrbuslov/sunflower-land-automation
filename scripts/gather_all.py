import asyncio

from resources_gathering.stones_mine import stones_plain_mine
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
            # "Cabbage Seed",
            # "Potato Seed",
            # "Pumpkin Seed",
        ]
        for crop_name in PLANTS_CULTURES_SEEDS_TO_PLANT:
            await plant_n_harvest(crop_name)

    async def _cut_down_trees():
        while True:
            if resources_settings.TOOLS_AMOUNT["Axe"] >= 0:
                await trees_cut_down()
                await asyncio.sleep(resources_settings.RESOURCES_WAITING_TIME['tree'])
            else:
                print('Not enough axes, waiting for you to buy (5 mins)...')
                # give time to buy axe
                await asyncio.sleep(60 * 5)
                resources_settings.update_session_data()

    async def _mine_stones():
        while True:
            if resources_settings.TOOLS_AMOUNT["Pickaxe"] >= 0:
                await stones_plain_mine()
                await asyncio.sleep(resources_settings.RESOURCES_WAITING_TIME['stone'])
            else:
                print('Not enough pickaxes, waiting for you to buy (7 mins)...')
                # give time to buy pickaxe
                await asyncio.sleep(60 * 7)
                resources_settings.update_session_data()

    tasks = [
        asyncio.create_task(_plant_n_harvest()),
        asyncio.create_task(_cut_down_trees()),
        asyncio.create_task(_mine_stones()),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(gather_all())
