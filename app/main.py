from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import config

app = FastAPI(title=config.APP_NAME)

app.include_router(api_router, prefix=config.API_V1_PREFIX)
