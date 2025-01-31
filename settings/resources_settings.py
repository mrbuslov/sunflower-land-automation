from settings.account_settings import AccountSettings


class ResourcesSettings(AccountSettings):
    LAND_HOLES: list[int] = []
    TREES: list[int] = []
    STONES: list[int] = []
    IRON_STONES: list[int] = []
    GOLD_STONES: list[int] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        session_data = self.get_session_file_data()

        self.LAND_HOLES = list(session_data['farm']['crops'].keys())
        self.TREES = list(session_data['farm']['trees'].keys())
        self.STONES = list(session_data['farm']['stones'].keys())
        self.IRON_STONES = list(session_data['farm']['iron'].keys())
        self.GOLD_STONES = list(session_data['farm']['gold'].keys())


resources_settings = ResourcesSettings()
