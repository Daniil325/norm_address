from dataclasses import dataclass

from norm_address.domain.protocols import AddressGateway


@dataclass
class NormalizeAddressCommand:
    address_gw: AddressGateway

    async def __call__(self, address: str) -> str:
        return await self.address_gw.get_address(address)
