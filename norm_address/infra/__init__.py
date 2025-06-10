from typing import AsyncIterator

from dishka import Provider, alias, provide, Scope
from dadata import DadataAsync
from redis.asyncio import Redis

from norm_address.domain.protocols import AddressGateway
from norm_address.infra.gateway import DadataGateway
from norm_address.infra.protocols import RedisRepo
from norm_address.infra.redis import RedisImpl
from norm_address.settings import Settings


class DadataProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    @provide
    async def get_dadata_client(self) -> AsyncIterator[DadataGateway]:
        async with DadataAsync(
            self.settings.api_token, self.settings.secret_token
        ) as client:
            yield DadataGateway(client)

    dadata_client = alias(source=DadataGateway, provides=AddressGateway)


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
