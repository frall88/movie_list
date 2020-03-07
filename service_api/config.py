import logging
import os


class Config:
    DEBUG = False
    LOG_FORMAT = "%(asctime)s %(levelname)8s %(message)s "
    LOG_DATEFMT = "%Y-%m-%dT%H:%M:%S"
    LOG_LEVEL = logging.DEBUG
    CACHE_DEFAULT_TIMEOUT = 60

    MOVIE_HOST = "https://ghibliapi.herokuapp.com"


class ProdConfig(Config):
    """Production configuration."""

    LOG_LEVEL = logging.INFO


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True


ENV_2_CONFIG = {"dev": DevConfig, "prod": ProdConfig}


def runtime_config(config=None):
    if config is None:
        env = os.environ.get("APP_ENV", "dev")
        assert env in ENV_2_CONFIG, "Unknown APP_ENV value: " + env
        config = ENV_2_CONFIG[env]

    return config
