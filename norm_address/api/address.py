from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from norm_address.application.usecases import NormalizeAddressCommand
from norm_address.infra.protocols import RedisRepo


router = APIRouter(
    tags=["Address"], prefix="/normalize_address", route_class=DishkaRoute
)


@router.get("/")
async def normalize_address(address: str, cmd: FromDishka[NormalizeAddressCommand], redis: FromDishka[RedisRepo]):
    result = await cmd(address)
    await redis.set("aaa", "bbb")
    print(result)
    return "result"
