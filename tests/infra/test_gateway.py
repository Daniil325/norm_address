import asyncio
import pytest
from pytest_httpx import HTTPXMock

import httpx

from norm_address.infra.gateway import DadataAddressGateway


@pytest.mark.asyncio
async def test_gateway(httpx_mock: HTTPXMock):
    async def simulate_network_latency(request: httpx.Request):
        await asyncio.sleep(1)
        return httpx.Response(
            status_code=200, json=[{"result": "address value"}],
        )

    httpx_mock.add_callback(simulate_network_latency)

    async with httpx.AsyncClient(base_url="https://test_url") as client:
        dadata = DadataAddressGateway(client)
        result = await dadata.get_address("result")
        assert result == {"result": "address value"}

