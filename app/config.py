import os

FILEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.abspath(os.path.join(FILEDIR, os.pardir))
PARENTDIR = os.path.abspath(os.path.join(BASEDIR, os.pardir))

DB_NAME = "database.db"
DEV_DB_PATH = os.path.join(BASEDIR, DB_NAME)
PROD_DB_PATH = os.path.join(PARENTDIR, DB_NAME)


class Config:
    # Disable SQL stuff
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Secret Key
    SECRET_KEY = os.environ.get("SECRET_KEY", default="secret_key")
    # JWT Secret Key
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY", default="jwt-secret_key")
    # Disable JWT Token expiration
    JWT_ACCESS_TOKEN_EXPIRES = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEV_DB_PATH}"


class ProductionConfig(Config):
    ENV = "production"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{PROD_DB_PATH}"
