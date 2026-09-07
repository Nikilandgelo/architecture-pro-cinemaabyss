from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int
    monolith_url: str
    movies_service_url: str
    events_service_url: str
    gradual_migration: bool
    movies_migration_percent: int


settings = Settings()
