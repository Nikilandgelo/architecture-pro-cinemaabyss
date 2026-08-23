from functools import wraps
from random import random
from typing import Callable, Any

from fastapi.background import BackgroundTasks
from httpx import Headers as HTTPXHeaders
from starlette.requests import Request, QueryParams, Headers as StarletteHeaders
from starlette.responses import StreamingResponse

from proxy.adapters.http import http_client
from proxy.loggers import service_logger
from proxy.settings import settings


def process_base_route(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
            self: "APIGateway",
            *args: Any,
            request: Request,
            **kwargs: Any
    ) -> StreamingResponse:
        if not self.gradual_migration:
            service_logger.info(
                f"Gradual migration feature flag is disabled, request {func.__name__.upper()} "
                f"{request.url.path} go to monolith..."
            )
            response = await self._request(
                method=func.__name__.upper(),
                url=f"{settings.monolith_url}{request.url.path}",
                body=await request.body(),
                query=request.query_params,
                headers=request.headers,
                cookies=request.cookies
            )
            return response

        return await func(self, *args, request=request, **kwargs)

    return wrapper


class APIGateway:

    def __init__(self, *, gradual_migration: bool | None = None) -> None:
        self.gradual_migration = (
            gradual_migration
            if gradual_migration is not None
            else settings.gradual_migration
        )

    def _clear_headers(self, headers: StarletteHeaders) -> list[tuple[str, str]]:
        headers_for_remove = {"host", "content-length"}
        return [
            (header, value)
            for header, value in headers.items()
            if header.lower() not in headers_for_remove
        ]

    def _clear_response_headers(self, headers: HTTPXHeaders) -> list[tuple[str, str]]:
        headers_for_remove = {"transfer-encoding", "date"}
        return [
            (header, value)
            for header, value in headers.multi_items()
            if header.lower() not in headers_for_remove
        ]

    def _get_url(self, request: Request) -> str:
        if (settings.movies_migration_percent / 100) >= random():
            url = f"{settings.movies_service_url}{request.url.path}"
        else:
            url = f"{settings.monolith_url}{request.url.path}"

        return url

    async def _request(
            self,
            method: str,
            url: str,
            body: bytes,
            query: QueryParams,
            headers: StarletteHeaders,
            cookies: dict
    ) -> StreamingResponse:
        service_logger.info(f"Request {method.upper()} is going to {url} ...")
        request = http_client.build_request(
            method=method,
            url=url,
            content=body,
            params=query,
            headers=self._clear_headers(headers),
            cookies=cookies
        )
        response = await http_client.send(request=request, stream=True)
        streaming_response = StreamingResponse(
            content=response.aiter_raw(),
            status_code=response.status_code,
            background=BackgroundTasks([response.aclose])
        )
        for key, value in self._clear_response_headers(response.headers):
            streaming_response.headers.append(key, value)

        return streaming_response

    @process_base_route
    async def get(self, *, request: Request) -> StreamingResponse:
        response = await self._request(
            method="GET",
            url=self._get_url(request),
            body=await request.body(),
            query=request.query_params,
            headers=request.headers,
            cookies=request.cookies
        )
        return response

    @process_base_route
    async def post(self, *, request: Request) -> StreamingResponse:
        response = await self._request(
            method="POST",
            url=self._get_url(request),
            body=await request.body(),
            query=request.query_params,
            headers=request.headers,
            cookies=request.cookies
        )
        return response

    @process_base_route
    async def put(self, *, request: Request) -> StreamingResponse:
        response = await self._request(
            method="PUT",
            url=self._get_url(request),
            body=await request.body(),
            query=request.query_params,
            headers=request.headers,
            cookies=request.cookies
        )
        return response

    @process_base_route
    async def patch(self, *, request: Request) -> StreamingResponse:
        response = await self._request(
            method="PATCH",
            url=self._get_url(request),
            body=await request.body(),
            query=request.query_params,
            headers=request.headers,
            cookies=request.cookies
        )
        return response

    @process_base_route
    async def delete(self, *, request: Request) -> StreamingResponse:
        response = await self._request(
            method="DELETE",
            url=self._get_url(request),
            body=await request.body(),
            query=request.query_params,
            headers=request.headers,
            cookies=request.cookies
        )
        return response
