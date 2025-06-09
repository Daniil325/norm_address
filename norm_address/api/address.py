from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from norm_address.application.usecases import NormalizeAddressCommand


router = APIRouter(
    tags=["Address"], prefix="/normalize_address", route_class=DishkaRoute
)


@router.get("/")
async def normalize_address(address: str, cmd: FromDishka[NormalizeAddressCommand]):
    result = await cmd(address)
    print(result)
    return "result"
