from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int
    kafka_brokers: str

settings = Settings()
