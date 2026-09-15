from events.broker.routers import payment_router
from events.loggers import service_logger
from events.payloads import PaymentPayload


@payment_router.subscriber("", group_id="payment-events-group", title="Payment Events Consumer")
async def process_payment_event(msg: PaymentPayload):
    service_logger.info(msg.model_dump_json(indent=2))
