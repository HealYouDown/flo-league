from flask_login.utils import login_required, logout_user
from app.blueprints.auth.forms import LoginForm
from app.models import Moderator
from flask import Blueprint, redirect
from flask.helpers import url_for
from flask.templating import render_template
from flask_babel import gettext
from flask_login import current_user, login_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        mod = Moderator.query.filter(
            Moderator.username == form.username.data
        ).first()

        login_user(mod, remember=True)

        return redirect(url_for("moderating.index"))

    return render_template(
        "auth/login.html",
        title=gettext("Login"),
        form=form,
    )


@bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
