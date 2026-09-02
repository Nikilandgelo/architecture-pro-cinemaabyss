from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import StreamingResponse

from proxy.gateway import APIGateway

movies_router = APIRouter()


@movies_router.get("{any_path:path}")
async def get_movies(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway().get(request=request)


@movies_router.post("{any_path:path}", status_code=status.HTTP_201_CREATED)
async def post_movies(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway().post(request=request)


@movies_router.put("{any_path:path}")
async def put_movies(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway().put(request=request)


@movies_router.patch("{any_path:path}")
async def patch_movies(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway().patch(request=request)


@movies_router.delete("{any_path:path}")
async def delete_movies(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway().delete(request=request)
