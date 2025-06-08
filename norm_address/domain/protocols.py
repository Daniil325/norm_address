from abc import ABC, abstractmethod


class AddressGateway(ABC):

    @abstractmethod
    async def get_address(self, address: str) -> str: ...
