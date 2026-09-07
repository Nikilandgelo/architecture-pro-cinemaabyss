from uvicorn import run
from proxy.settings import settings


if __name__ == "__main__":
    run("proxy.app:app", host="0.0.0.0", port=settings.port, reload=True)
