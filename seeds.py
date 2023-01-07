from app.core.database import init_db_seeds
from tortoise import run_async, Tortoise
from app.core.user.seeds import run as user_seeds

async def init():
    await init_db_seeds()
    await Tortoise.generate_schemas()
    await user_seeds()

run_async(init())

