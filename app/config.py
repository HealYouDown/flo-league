import os

DB_NAME = "database.db"


class Config:
    # SQLALCHEMY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///../{DB_NAME}"

    # Secret Key
    SECRET_KEY = os.environ.get("SECRET_KEY", default="secret_key")

    # Languages
    LANGUAGES = ["en", "de", "fr", "it", "tr", "es", "pt"]
    BABEL_TRANSLATION_DIRECTORIES = "translation/translations"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

    # Disables caching
    SEND_FILE_MAX_AGE_DEFAULT = 0


class ProductionConfig(Config):
    ENV = "production"
