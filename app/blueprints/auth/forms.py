from app.models import Moderator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate_username(self, field: StringField) -> None:
        if not Moderator.query.filter(
                Moderator.username == field.data).count() == 1:
            raise ValidationError("User not found")

    def validate_password(self, field: PasswordField) -> None:
        mod = Moderator.query.filter(
            Moderator.username == self.username.data).first()
        if mod and mod.password != field.data:
            raise ValidationError("Password does not match.")
