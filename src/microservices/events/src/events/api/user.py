from fastapi import APIRouter, status

from events.broker.producers import user_publisher
from events.payloads import UserPayload
from events.responses import SuccessfulResponse

user_router = APIRouter()


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_event(body: UserPayload) -> SuccessfulResponse:
    await user_publisher.publish(body.model_dump_json().encode())
    return SuccessfulResponse()
