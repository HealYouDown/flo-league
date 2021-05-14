from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

login = LoginManager()
db = SQLAlchemy()
babel = Babel()
