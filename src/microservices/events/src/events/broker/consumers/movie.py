from events.broker.routers import movie_router
from events.loggers import service_logger
from events.payloads import MoviePayload


@movie_router.subscriber("", title="Movie Events Consumer")
async def process_movie_event(msg: MoviePayload):
    service_logger.info(msg.model_dump_json(indent=2))
