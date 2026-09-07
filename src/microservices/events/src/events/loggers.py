from logging import getLogger, INFO, Logger, StreamHandler, Formatter


def setup_logger(logger_name: str, log_level: int = INFO) -> Logger:
    logger = getLogger(logger_name)
    logger.propagate = False
    logger.setLevel(log_level)
    if logger.hasHandlers():
        return logger

    handler = StreamHandler()
    handler.setFormatter(
        Formatter(
            style="{",
            fmt="[{name}] {asctime}: {levelname} - {message}",
        )
    )
    logger.addHandler(handler)
    return logger


service_logger = setup_logger("EVENTS")
