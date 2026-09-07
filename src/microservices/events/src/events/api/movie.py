from fastapi import APIRouter, status

from events.broker.producers import movie_publisher
from events.payloads import MoviePayload
from events.responses import SuccessfulResponse

movie_router = APIRouter()


@movie_router.post("", status_code=status.HTTP_201_CREATED)
async def create_movie_event(body: MoviePayload) -> SuccessfulResponse:
    await movie_publisher.publish(body.model_dump_json().encode())
    return SuccessfulResponse()
