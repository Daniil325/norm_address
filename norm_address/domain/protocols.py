from abc import ABC, abstractmethod
from typing import Any


class AddressGateway(ABC):

    @abstractmethod
    async def get_address(self, address: str) -> dict[str, Any]: ...
