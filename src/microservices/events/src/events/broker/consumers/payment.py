from events.broker.routers import payment_router
from events.loggers import service_logger
from events.payloads import PaymentPayload


@payment_router.subscriber("", title="Payment Events Consumer")
async def process_payment_event(msg: PaymentPayload):
    service_logger.info(msg.model_dump_json(indent=2))
