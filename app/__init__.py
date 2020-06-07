from flask import Flask

from app.api.routes import api_bp
from app.main.routes import main_bp
from app.config import DevelopmentConfig, ProductionConfig
from app.extensions import db, jwt
from app.jwt_loader import user_loader
from app.converter import RegexConverter


def create_app(development: bool = False) -> Flask:
    app = Flask(__name__)

    # Config
    if development:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Extensions
    db.init_app(app)
    jwt.init_app(app)

    # Extensions options
    jwt._user_loader_callback = user_loader

    # Register Regex converter
    app.url_map.converters["regex"] = RegexConverter

    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
