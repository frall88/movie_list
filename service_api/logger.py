import logging


def init_logging(
    log_format: str = "[%(levelname)s] [%(asctime)s] %(message)s", log_level: str = logging.INFO, config=None
):
    """Set logger configuration and handler.

    Args:
        log_format: logging message format string.
        log_level: logging level.
        config: application config.

    """
    config = config or {}
    log_msg_format = config.get("LOG_FORMAT", log_format)
    log_date_format = config.get("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")
    log_level = config.get("LOG_LEVEL", log_level)

    handler = logging.StreamHandler()
    logger = logging.getLogger("")
    if len(logger.handlers) == 0:
        logger.addHandler(handler)

    formatter = logging.Formatter(log_msg_format, log_date_format)
    logger.handlers[0].setFormatter(formatter)
    logger.setLevel(log_level)
