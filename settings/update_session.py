from settings.account_settings import account_settings


def update_session_file() -> None:
    account_settings.get_session_data(force_update_session=True)


if __name__ == "__main__":
    update_session_file()
