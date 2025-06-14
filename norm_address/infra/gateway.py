from typing import Any
from httpx import AsyncClient
from norm_address.domain.protocols import AddressGateway


class DadataAddressGateway(AddressGateway):

    def __init__(self, client: AsyncClient):
        self._client = client

    async def get_address(self, address: str) -> dict[str, Any]:
        result = await self._client.post(self._client.base_url, json=[address])
        post_response = result.json()
        return post_response[0]
