from events.payloads import MoviePayload, UserPayload, PaymentPayload
from .routers import movie_router, payment_router, user_router

movie_publisher = movie_router.publisher(
    topic="",
    title="Movie Events Publisher",
    schema=MoviePayload
)
payment_publisher = payment_router.publisher(
    topic="",
    title="Payment Events Publisher",
    schema=PaymentPayload
)
user_publisher = user_router.publisher(
    topic="",
    title="User Events Publisher",
    schema=UserPayload
)
