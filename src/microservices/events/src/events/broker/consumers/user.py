from events.broker.routers import user_router
from events.loggers import service_logger
from events.payloads import UserPayload


@user_router.subscriber("", title="User Events Consumer")
async def process_user_event(msg: UserPayload):
    service_logger.info(msg.model_dump_json(indent=2))
