import logging
from fastapi import APIRouter

from src.bff.dto import FeedPage
from src.misc.pagination import Page

_LOGGER = logging.getLogger(__file__)

router = APIRouter(prefix="", tags=["backend-for-frontend"])

@router.get("/feed")
async def get_feed(
) -> Page[FeedPage]:
    _LOGGER.info(f"Requesting latest feed")

    return []
    
