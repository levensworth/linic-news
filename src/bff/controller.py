import logging
from fastapi import APIRouter

from src.misc.pagination import Page

_LOGGER = logging.getLogger(__file__)

router = APIRouter(prefix="", tags=["backend-for-frontend"])

@router.get("/feed")
async def get_feed(
) -> Page[str]:
    _LOGGER.info("Requesting latest feed")

    return Page.empty(str)
    
