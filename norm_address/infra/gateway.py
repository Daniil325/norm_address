from norm_address.domain.protocols import AddressGateway


class DadataGateway(AddressGateway):

    def __init__(self, client):
        self._client = client

    async def get_address(self, address: str) -> str:
        result = await self._client.clean("address", address)
        return result
