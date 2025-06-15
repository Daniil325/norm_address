from pathlib import Path
from typing import AsyncIterator

from dishka import AsyncContainer, Provider, Scope, alias, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient
import httpx
import respx
import pytest

from norm_address.app import create_app
from norm_address.application import CommandsProvider
from norm_address.domain.protocols import AddressGateway
from norm_address.infra import RedisProvider
from norm_address.infra.gateway import DadataAddressGateway
from norm_address.settings import Settings
from redis.asyncio import Redis


@pytest.fixture
async def mocked_api():
    async with respx.mock(base_url="https://foo.bar", assert_all_called=False) as respx_mock:
        # Predefine a route for "/users/"
        users_route = respx_mock.post("/", name="list_users")
        users_route.return_value = httpx.Response(200, json=[{"result": "address value"}])
        yield respx_mock


class MockDadataProvider(Provider):
    scope = Scope.REQUEST
    
    def __init__(self):
        super().__init__()
        
    @provide
    async def get_dadata_client(self) -> AsyncIterator[DadataAddressGateway]:
        async with httpx.AsyncClient(base_url="https://foo.bar") as client:
            yield DadataAddressGateway(client)
    
    dadata_client = alias(source=DadataAddressGateway, provides=AddressGateway)


here = Path(__file__).parent


def pytest_addoption(parser):
    parser.addini("redis_uri", "URI for test redis instance")


@pytest.fixture(scope="session")
def fixtures_path():
    return Path(here).joinpath("fixtures")


@pytest.fixture
async def redis(request):
    redis_instance = Redis.from_url(request.config.getini("redis_uri"))
    await redis_instance.flushall()
    return redis_instance


@pytest.fixture
async def container(request, mocked_api) -> AsyncContainer:
    settings = Settings(api_token="", secret_token="", redis_url=request.config.getini("redis_uri"))
    return make_async_container(
        CommandsProvider(), MockDadataProvider(), RedisProvider(settings)
    )


@pytest.fixture
async def app(container):
    app = create_app()
    setup_dishka(container, app)
    return app


@pytest.fixture
async def client(app):
    with TestClient(app) as client:
        yield client
