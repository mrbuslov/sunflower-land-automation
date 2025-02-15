import httpx

from settings.account_settings import account_settings
from utils.consts import DEFAULT_HEADERS
from utils.schemas import ApiRouter


async def send_data(data: dict) -> httpx.Response:
    account_settings.is_operation_performing = True
    async with httpx.AsyncClient() as client:
        response = await client.post(ApiRouter.AUTOSAVE, headers=DEFAULT_HEADERS(), json=data)
        account_settings.is_operation_performing = False
        response.raise_for_status()
        return response
