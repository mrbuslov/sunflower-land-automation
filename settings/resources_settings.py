from settings.account_settings import AccountSettings


class ResourcesSettings(AccountSettings):
    LAND_HOLES: list[str] = []
    TREES: list[str] = []
    STONES: list[str] = []
    IRON_STONES: list[str] = []
    GOLD_STONES: list[str] = []

    LAND_HOLES_AVAILABILITY: dict[str, bool] = {}

    CROPS_AMOUNT: dict[str, float] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        session_data = self.get_session_file_data()

        self.LAND_HOLES = list(session_data['farm']['crops'].keys())
        self.TREES = list(session_data['farm']['trees'].keys())
        self.STONES = list(session_data['farm']['stones'].keys())
        self.IRON_STONES = list(session_data['farm']['iron'].keys())
        self.GOLD_STONES = list(session_data['farm']['gold'].keys())

        self.LAND_HOLES_AVAILABILITY = {
            hole: not bool(session_data['farm']['crops'][hole].get('crop', False))
            for hole in self.LAND_HOLES
        }
        self.CROPS_AMOUNT = {
            key: float(value)
            for key, value in session_data['farm']["inventory"].items()
        }

    def is_able_to_plant(self, amount: int) -> bool:
        """Check if there are enough land holes to plant"""
        if amount == -1:
            return sum(self.LAND_HOLES_AVAILABILITY.values()) > 0
        return sum(self.LAND_HOLES_AVAILABILITY.values()) >= amount

    def is_crops_amount_sufficient(self, name: str, amount: int) -> bool:
        """Check if crops amount is sufficient"""
        if amount == -1:
            return int(self.CROPS_AMOUNT[name]) > 0
        return self.CROPS_AMOUNT[name] >= amount


resources_settings = ResourcesSettings()
