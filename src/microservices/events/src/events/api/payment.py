from fastapi import APIRouter, status

from events.broker.producers import payment_publisher
from events.payloads import PaymentPayload
from events.responses import SuccessfulResponse

payment_router = APIRouter()


@payment_router.post("", status_code=status.HTTP_201_CREATED)
async def create_payment_event(body: PaymentPayload) -> SuccessfulResponse:
    await payment_publisher.publish(body.model_dump_json().encode())
    return SuccessfulResponse()
