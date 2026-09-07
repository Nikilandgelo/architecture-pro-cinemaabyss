from fastapi import APIRouter

from .default import default_router
from .movies import movies_router

api_router = APIRouter(prefix="/api")

api_router.include_router(movies_router, prefix="/movies", tags=["Movies"])

# Order matters! All endpoints that shouldn't be proxied somewhere beside monolith must be below
api_router.include_router(default_router, prefix="", tags=["Default"])
