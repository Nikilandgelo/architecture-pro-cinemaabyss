from fastapi import APIRouter

from .movie import movie_router
from .payment import payment_router
from .user import user_router

router = APIRouter(prefix="/api/events")
router.include_router(movie_router, prefix="/movie", tags=["Movie"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(payment_router, prefix="/payment", tags=["Payment"])


@router.get("/health", tags=["Health"])
async def health():
    return {"status": True}
