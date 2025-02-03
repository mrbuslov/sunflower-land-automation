from settings.account_settings import account_settings


def update_session_file() -> None:
    account_settings.update_session_data()


if __name__ == "__main__":
    update_session_file()
