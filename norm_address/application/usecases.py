from dataclasses import dataclass

from norm_address.domain.protocols import AddressGateway
from norm_address.infra.protocols import RedisRepo


@dataclass
class NormalizeAddressCommand:
    address_gw: AddressGateway
    redis_repo: RedisRepo

    async def __call__(self, address: str) -> str | None:
        if await self.redis_repo.get(address):
            return (await self.redis_repo.get(address)).decode()
        
        response = await self.address_gw.get_address(address)
        result = response["result"]
        if result:
            await self.redis_repo.set(address, result)
        return result
