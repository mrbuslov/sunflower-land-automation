import asyncio

from resources_gathering.harvest import harvest
from resources_gathering.restock import restock
from resources_gathering.stones_mine import stones_plain_mine
from resources_gathering.trees_cut import trees_cut_down
from scripts.plant_n_harvest import plant_n_harvest
from settings.account_settings import account_settings
from settings.resources_settings import resources_settings
from utils.utils import run_w_delay_wrapper


async def gather_all():
    """
    Gathers all crops + resources
    """

    async def _plant_n_harvest():
        account_settings.update_session_data()
        await restock()
        await asyncio.sleep(5)
        account_settings.update_session_data()
        await harvest()
        await asyncio.sleep(10)
        PLANTS_CULTURES_SEEDS_TO_PLANT = [
            "Sunflower Seed",
            "Rhubarb Seed",
            "Carrot Seed",
            # "Cabbage Seed",
            # "Potato Seed",
            # "Pumpkin Seed",
        ]
        for crop_name in PLANTS_CULTURES_SEEDS_TO_PLANT:
            account_settings.update_session_data()
            await plant_n_harvest(crop_name)

    async def _cut_down_trees():
        account_settings.update_session_data()
        while True:
            if resources_settings.TOOLS_AMOUNT["Axe"] >= 0:
                await trees_cut_down()
                await asyncio.sleep(resources_settings.RESOURCES_WAITING_TIME['tree'])
            else:
                # give time to buy axe
                print('Not enough axes, waiting for you to buy (5 mins)...')
                await asyncio.sleep(60 * 5)
                account_settings.update_session_data()

    async def _mine_stones():
        account_settings.update_session_data()
        while True:
            if resources_settings.TOOLS_AMOUNT["Pickaxe"] >= 0:
                await stones_plain_mine()
                await asyncio.sleep(resources_settings.RESOURCES_WAITING_TIME['stone'])
            else:
                # give time to buy pickaxe
                print('Not enough pickaxes, waiting for you to buy (7 mins)...')
                await asyncio.sleep(60 * 7)
                account_settings.update_session_data()

    tasks = [
        run_w_delay_wrapper(0, _plant_n_harvest()),
        run_w_delay_wrapper(30, _cut_down_trees()),
        run_w_delay_wrapper(45, _mine_stones()),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(gather_all())
