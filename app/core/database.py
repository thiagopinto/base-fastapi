from app.core.config import settings
from pydantic import PostgresDsn
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise


POSTGRES_DSN = PostgresDsn.build(
    scheme=settings.DBAPI,
    user=settings.USER_DATABASE,
    password=settings.PASS_DATABASE,
    host=f"{settings.HOST_DATABASE}:{settings.PORT_DATABASE}",
    path=f"/{settings.DATABASE_NAME or ''}",
)


TORTOISE_ORM = {
    "connections": {"default": str(POSTGRES_DSN)},
    "apps": {
        "models": {
            "models": ["aerich.models", "app.core.user.models"],
            "default_connection": "default",
        },
    },
}

def init_db(app):
    register_tortoise(
        app,
        db_url=str(POSTGRES_DSN),
        modules={"models": ["app.core.user.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

async def init_db_seeds():
    await Tortoise.init(
        db_url=str(POSTGRES_DSN),
        modules={"models": ["app.core.user.models"]}
    )
    print("Initialized connection")