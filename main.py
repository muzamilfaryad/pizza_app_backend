from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints import auth_router, orders_router
from core.config import settings
from core.database import engine
from models.order import Order
from models.user import Base, User


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> dict:
    return {
        "message": "Pizza App API is running",
    }


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
    }


app.include_router(auth_router)
app.include_router(orders_router)