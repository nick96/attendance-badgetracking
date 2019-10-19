import os
from datetime import timedelta


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("APP_SECRET", "secret-key")

    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, (os.pardir)))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@admin.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

    JWT_AUTH_HEADER_PREFIX = "Bearer"
    JWT_AUTH_USERNAME_KEY = "sub"
    JWT_EXP_SEC = timedelta(hours=24).total_seconds()
    JWT_ALGOS = ["HS256"]
    JWT_SECRET = os.environ.get("JWT_SECRET", "secret")


class ProdConfig(Config):
    ENV = "prod"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


class DevConfig(Config):
    ENV = "dev"
    DEBUG = True
    DB_NAME = "dev.db"
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    ARGON_ROUNDS = 4


def config() -> Config:
    if os.environ.get("CI"):
        return TestConfig()
    elif os.environ.get("FLASK_ENV") == "development":
        return DevConfig()
    return ProdConfig()
