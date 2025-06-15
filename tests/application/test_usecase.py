import pytest

from norm_address.application.usecases import NormalizeAddressCommand
from norm_address.domain.protocols import AddressGateway
from norm_address.infra.protocols import RedisRepo


@pytest.mark.unit
async def test_normalize_address_from_gw(mocker, redis):
    address_gw = mocker.AsyncMock(spec=AddressGateway)
    address_gw.get_address = mocker.AsyncMock(return_value={"result": "from address gw"})
    redis_repo = mocker.AsyncMock(spec=RedisRepo)
    redis_repo.get = mocker.AsyncMock(return_value=None)

    sut = NormalizeAddressCommand(address_gw=address_gw, redis_repo=redis_repo)
    
    result = await sut("12345")
    
    assert result == "from address gw"
    
    
@pytest.mark.unit
async def test_normalize_address_from_redis(mocker, redis):
    address_gw = mocker.AsyncMock(spec=AddressGateway)
    address_gw.get_address = mocker.AsyncMock(return_value={"result": "from address gw"})
    redis_repo = mocker.AsyncMock(spec=RedisRepo)
    redis_repo.get = mocker.AsyncMock(return_value=b"address from redis")
    
    sut = NormalizeAddressCommand(address_gw=address_gw, redis_repo=redis_repo)
    
    result = await sut("12345")
    
    assert result == "address from redis"