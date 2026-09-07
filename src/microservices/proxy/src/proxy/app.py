from contextlib import asynccontextmanager

from fastapi import FastAPI

from proxy.adapters.http import http_client
from proxy.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await http_client.aclose()


app = FastAPI(
    title="API Gateway Proxy Service",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
