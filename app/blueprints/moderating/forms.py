from app.enums import CharacterClass, Server, TeamSize
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, IntegerField, SelectField
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired
from wtforms.widgets.core import HiddenInput


class CreateMatchesForm(FlaskForm):
    team_size = SelectField("Team Size", choices=[
        (TeamSize.one_vs_one.value, "1 vs. 1"),
        (TeamSize.two_vs_two.value, "2 vs. 2"),
        (TeamSize.three_vs_three.value, "3 vs. 3"),
    ])
    is_ranked = BooleanField("Is ranked?", default=True)
    make_teams_fair = BooleanField("Teams fair?", default=True)

    player_ids = FieldList(IntegerField("Player ID", widget=HiddenInput()))


class PlayerForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    guild = StringField("Guild")
    character_class = SelectField("Class", choices=[
        (CharacterClass.noble.value, "Noble"),
        (CharacterClass.magic_knight.value, "Magic Knight"),
        (CharacterClass.court_magician.value, "Court Magician"),
        (CharacterClass.explorer.value, "Explorer"),
        (CharacterClass.sniper.value, "Sniper"),
        (CharacterClass.excavator.value, "Excavator"),
        (CharacterClass.saint.value, "Saint"),
        (CharacterClass.shaman.value, "Shaman"),
        (CharacterClass.priest.value, "Priest"),
        (CharacterClass.mercenary.value, "Mercenary"),
        (CharacterClass.guardian_swordsman.value, "Guardian Swordsman"),
        (CharacterClass.gladiator.value, "Gladiator"),
    ])
    server = SelectField("Server", choices=[
        (Server.bergruen.value, "Bergruen"),
        (Server.luxplena.value, "LuxPlena"),
    ])
    level_land = IntegerField("Level Land")
    level_sea = IntegerField("Level Sea")
