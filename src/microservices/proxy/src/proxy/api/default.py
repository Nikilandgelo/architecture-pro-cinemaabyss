from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import StreamingResponse

from proxy.gateway import APIGateway

default_router = APIRouter()


@default_router.get("{any_path:path}")
async def get_endpoint(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway(gradual_migration=False).get(request=request)


@default_router.post("{any_path:path}", status_code=status.HTTP_201_CREATED)
async def post_endpoint(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway(gradual_migration=False).post(request=request)


@default_router.put("{any_path:path}")
async def put_endpoint(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway(gradual_migration=False).put(request=request)


@default_router.patch("{any_path:path}")
async def patch_endpoint(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway(gradual_migration=False).patch(request=request)


@default_router.delete("{any_path:path}")
async def delete_endpoint(request: Request, any_path: str) -> StreamingResponse:
    return await APIGateway(gradual_migration=False).delete(request=request)
