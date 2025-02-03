import functools

import requests

from settings.account_settings import account_settings


def handle_gathering_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
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
                        return func(*args, **kwargs)
                except ValueError:
                    pass  # Response was not in JSON format
    return wrapper
