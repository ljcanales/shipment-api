from fastapi import FastAPI

from app.api.tracking import router
from app.core.middleware import TraceMiddleware
from app.core.logging import configure_logging

app = FastAPI()
configure_logging()
app.add_middleware(TraceMiddleware)
app.include_router(router)
