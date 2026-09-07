from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.asgi import make_ping_asgi, make_asyncapi_asgi
from faststream.kafka import KafkaBroker
from faststream.specification import AsyncAPI

from events.api import router
from events.broker import kafka_router
from events.settings import settings

broker = KafkaBroker(bootstrap_servers=settings.kafka_brokers)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with broker:
        await broker.start()
        yield


app = FastAPI(
    title="Events API",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(router)
broker.include_router(kafka_router)

app.mount("/health", make_ping_asgi(broker, timeout=5.0))
app.mount(
    "/asyncapi",
    make_asyncapi_asgi(
        AsyncAPI(
            broker,
            title="Events Broker",
            version="1.0.0",
        ),
        try_it_out_path=None)
)
