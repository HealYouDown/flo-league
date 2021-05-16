from app.enums import Winner
from app.utils import next_weekday
from flask import Flask

from app.blueprints.auth.user_loader import load_user
from app.blueprints.auth.views import bp as auth_bp
from app.blueprints.main.views import bp as main_bp
from app.blueprints.moderating.views import bp as moderating_bp
from app.config import DevelopmentConfig, ProductionConfig
from app.constants import FIRST_DATE, LAST_DATE, SEASON
from app.extensions import babel, db, login
from app.translation.localeselector import get_locale
from app.translation.set_language import set_language_endpoint
from flask_babel import format_date


def create_app(development: bool = False) -> Flask:
    # Create flask application object
    app = Flask(__name__)

    # Set the application config
    if development:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Jinja2 flags env
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # Register extensions
    register_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Flask-Login specifics
    login.user_loader(load_user)

    # Babel specifics
    babel.localeselector(get_locale)
    # register a route to set language cookie
    app.add_url_rule("/set-lang/<lang>", "set_lang", set_language_endpoint)

    # Add variables or functions to jinja2 context
    app.context_processor(lambda: {
        "get_locale": get_locale,
        "format_date": format_date,
        "next_weekday": next_weekday,
        "Winner": Winner,
        "SEASON": SEASON,
        "FIRST_DATE": FIRST_DATE,
        "LAST_DATE": LAST_DATE,
    })

    # Create database
    with app.app_context():
        db.create_all()

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    login.init_app(app)
    babel.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(moderating_bp)
