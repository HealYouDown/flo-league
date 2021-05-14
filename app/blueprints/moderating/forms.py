from app.enums import TeamSize
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, IntegerField, SelectField
from wtforms.widgets.core import HiddenInput


class CreateMatchesForm(FlaskForm):
    mode_select = SelectField("Modus", choices=[
        (TeamSize.one_vs_one.value, "1 vs. 1"),
        (TeamSize.two_vs_two.value, "2 vs. 2"),
        (TeamSize.three_vs_three.value, "3 vs. 3"),
    ])
    is_ranked = BooleanField("Is ranked?", default=True)
    make_teams_fair = BooleanField("Teams fair?", default=True)

    player_ids = FieldList(IntegerField("Player ID", widget=HiddenInput()))
