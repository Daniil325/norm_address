from dataclasses import dataclass

from norm_address.domain.protocols import AddressGateway
from norm_address.infra.protocols import RedisRepo
from norm_address.infra.logging import logger


@dataclass
class NormalizeAddressCommand:
    address_gw: AddressGateway
    redis_repo: RedisRepo

    async def __call__(self, address: str) -> str | None:
        if await self.redis_repo.get(address):
            logger.info("Get address from redis storage")
            return (await self.redis_repo.get(address)).decode()
        
        logger.info("Get address from dadata api")
        response = await self.address_gw.get_address(address)
        print("dddd", response)
        result = response["result"]
        if result:
            logger.info("Set address to redis storage")
            await self.redis_repo.set(address, result)
        return result
