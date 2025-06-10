from typing import AsyncIterator

from dishka import Provider, alias, provide, Scope
from httpx import AsyncClient
from redis.asyncio import Redis

from norm_address.domain.protocols import AddressGateway
from norm_address.infra.gateway import DadataAddressGateway
from norm_address.infra.protocols import RedisRepo
from norm_address.infra.redis import RedisImpl
from norm_address.settings import Settings


class DadataProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    @provide
    async def get_dadata_client(self) -> AsyncIterator[DadataAddressGateway]:
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.settings.api_token}",
            "X-Secret": self.settings.secret_token
        }
        async with AsyncClient(base_url="https://cleaner.dadata.ru/api/v1/clean/address", headers=headers) as client:
            yield DadataAddressGateway(client)

    dadata_client = alias(source=DadataAddressGateway, provides=AddressGateway)


class RedisProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    @provide
    def get_redis(self) -> Redis:
        return Redis.from_url(self.settings.redis_url)

    @provide
    async def get_redis_repo(self, redis: Redis) -> RedisRepo:
        return RedisImpl(redis)
