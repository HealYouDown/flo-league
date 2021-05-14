import os

DB_NAME = "database.db"


class Config:
    # Disable SQL stuff
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret Key
    SECRET_KEY = os.environ.get("SECRET_KEY", default="secret_key")

    # Languages
    LANGUAGES = ["en", "de", "fr", "it", "tr", "es", "pt"]


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f"sqlite:///../{DB_NAME}"

    # Disables caching
    SEND_FILE_MAX_AGE_DEFAULT = 0


class ProductionConfig(Config):
    ENV = "production"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///../{DB_NAME}"
