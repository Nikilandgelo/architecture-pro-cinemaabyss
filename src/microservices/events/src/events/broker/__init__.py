from faststream.kafka import KafkaRouter

from .consumers import *
from .routers import movie_router, payment_router, user_router

kafka_router = KafkaRouter()
kafka_router.include_router(movie_router, prefix="movie-events")
kafka_router.include_router(payment_router, prefix="payment-events")
kafka_router.include_router(user_router, prefix="user-events")
