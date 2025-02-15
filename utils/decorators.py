import asyncio
import functools
import random

import requests

from settings.account_settings import account_settings


def handle_gathering_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print('---------- ERROR ----------')
            print('ERROR: ', e.response)
            if hasattr(e.response, 'status_code') and e.response.status_code == 500:
                try:
                    response_json = e.response.json()
                    print('response_json:', response_json)
                    if response_json.get('error') == 'MULTIPLE_DEVICES_OPEN':
                        print('Requesting session file to continue gathering...')
                        # request session file
                        account_settings.update_session_data()
                        return await func(*args, **kwargs)
                except ValueError:
                    pass  # Response was not in JSON format

    return wrapper


def wait_if_operation_performing(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if account_settings.is_operation_performing:
            seconds_to_wait = random.randint(1, 10)
            print(f'Operation is already in progress. Waiting {seconds_to_wait} seconds...')
            await asyncio.sleep(seconds_to_wait)
        return await func(*args, **kwargs)

    return wrapper
