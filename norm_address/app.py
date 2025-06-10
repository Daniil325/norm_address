from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from norm_address.application import CommandsProvider
from norm_address.infra import DadataProvider, RedisProvider
from norm_address.settings import Settings
from norm_address.api.address import router


def create_app():
    app = FastAPI()
    settings = Settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    
    container = make_async_container(
        CommandsProvider(),
        DadataProvider(settings),
        RedisProvider(settings)
    )
    
    setup_dishka(container, app)

    return app
