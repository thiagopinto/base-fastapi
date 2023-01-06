from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.core.config import settings
from app.core.database import init_db
from app.core.routers import router as core_router
from app.core.user.routers import router as user_router


def get_application():
    _app = FastAPI(title=settings.APP_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(core_router)
    _app.include_router(user_router)
    init_db(_app)
    

    return _app


app = get_application()