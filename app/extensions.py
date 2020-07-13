from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()
jwt = JWTManager()
admin = Admin(name="FloLeague", template_mode="bootstrap3")
