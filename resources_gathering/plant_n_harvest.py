# WIP (work in progress)
from resources_gathering.harvest import harvest
from resources_gathering.plant import plant
from settings.resources_settings import resources_settings
from utils.utils import divide_items_to_chunks, arg_parser_harvest


def plant_n_harvest(crop_name: str):
    """
    Plants seeds and harvests them immediately.
    NOTE: it plants seeds in past, so it can be easy to harvest. WORKS ONLY FOR THE PERIOD THAT SEEDS WERE NOT PLANTED
    You MUST keep old session file. For this you can use `.env` variable `SHOULD_REFRESH_SESSION=False`

    Every time we plant the crop and harvest it, we change land hole's "createdAt". So we can't plant all crops in one go.
    So we must calculate the time for each crop: plant time + grow time = harvest time
    """
    print('Starting planting n harvesting process...')
    print(f'Planting {resources_settings.CROPS_AMOUNT[crop_name]} {crop_name}')
    # divide by holes amount
    chunks_list = divide_items_to_chunks(
        resources_settings.CROPS_AMOUNT[crop_name],
        len(resources_settings.LAND_HOLES)
    )

    # for chunk in chunks_list:
    chunk = 10
    print(f'Planting {chunk} {crop_name}')
    plant(crop_name, chunk)
    print(f'Harvesting {chunk} {crop_name}')
    harvest(crop_name)
    print('-' * 80)


if __name__ == '__main__':
    args = arg_parser_harvest()
    plant_n_harvest(args.name)
