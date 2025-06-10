from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Depends, HTTPException

from norm_address.api.base import AddressResponseItem
from norm_address.application.usecases import NormalizeAddressCommand
from norm_address.infra.logging import logger


router = APIRouter(
    tags=["Address"], prefix="/normalize_address", route_class=DishkaRoute
)


def check_address_len(address: str):
    if len(address) >= 60:
        logger.error("Address length longer than 60")
        raise HTTPException(status_code=400, detail="Превышена длина входного запроса")
    return address


@router.get("/", response_model=AddressResponseItem)
async def normalize_address(
    cmd: FromDishka[NormalizeAddressCommand], address: str = Depends(check_address_len)
):
    result = await cmd(address)
    return {"result": result}
