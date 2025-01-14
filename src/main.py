from contextlib import asynccontextmanager
import logging
import typing
from fastapi import APIRouter, FastAPI
from src.bindings import Container
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from apscheduler.triggers.interval import IntervalTrigger  # type: ignore

# ROUTING

app_router = APIRouter()

logging.basicConfig(
    level="INFO",
    format="[%(asctime)s] - "
    "[%(levelname)s] - "
    "%(filename)s =>  "
    "%(funcName)s(): "
    "(line %(lineno)d)\t"
    "%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> typing.AsyncGenerator[None, None]:
    # Create and start the AsyncIOScheduler
    scheduler = AsyncIOScheduler()
    scheduler.start()

    # Schedule the async task to run every 10 minutes

    yield
    print("Shutting down scheduler...")
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(app_router)

setattr(app, "container", Container())
