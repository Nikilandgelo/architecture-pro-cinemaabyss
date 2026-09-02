from uvicorn import run
from events.settings import settings


if __name__ == "__main__":
    run("events.app:app", host="0.0.0.0", port=settings.port, reload=True)
