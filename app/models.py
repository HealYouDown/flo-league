import datetime

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from app.enums import CharacterClass, Server, Winner
from app.extensions import db
from flask_login import UserMixin
from app.constants import SEASON


class Player(db.Model):
    __tablename__ = "player"

    id = Column(Integer, autoincrement=True, primary_key=True)

    username = Column(String(13), nullable=False)
    guild = Column(String(16))
    character_class = Column(Enum(CharacterClass), nullable=False)
    server = Column(Enum(Server), nullable=False)
    level_land = Column(Integer, nullable=False)
    level_sea = Column(Integer, nullable=False)

    exists = Column(Boolean, default=True)

    statistics = relationship(
        "PlayerStatistics", order_by="PlayerStatistics.season.asc()",
    )

    def __repr__(self) -> str:
        return (
            "<Player "
            f"name={self.username} "
            f"class={self.character_class.value}"
            ">"
        )

    def to_dict(self) -> dict:
        return {
           "id": self.id,
           "username": self.username,
           # guild removed because tojson filter from flask
           # does not support some symbols in there
           # "guild": self.guild,
           "character_class": {
               "name": self.character_class.name,
               "value": self.character_class.value,
           },
           "server": {
               "name": self.server.name,
               "value": self.server.value,
           },
           "level_land": self.level_land,
           "level_sea": self.level_sea,
        }


class PlayerStatistics(db.Model):
    __tablename__ = "player_statistics"

    index = Column(Integer, autoincrement=True, primary_key=True)

    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    season = Column(Integer, nullable=False)

    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)

    points = Column(Integer, default=1000)


class RunningMatch(db.Model):
    __tablename__ = "running_match"

    id = Column(Integer, autoincrement=True, primary_key=True)
    server = Column(Enum(Server), nullable=False)
    is_ranked = Column(Boolean, default=True)

    team_1 = relationship(
        "RunningMatchParticipant", uselist=True,
        primaryjoin=(
            "and_("
            "foreign(RunningMatchParticipant.match_id) == RunningMatch.id,"
            "foreign(RunningMatchParticipant.team) == 0"
            ")"
        ),
        viewonly=True,
    )

    team_2 = relationship(
        "RunningMatchParticipant", uselist=True,
        primaryjoin=(
            "and_("
            "foreign(RunningMatchParticipant.match_id) == RunningMatch.id,"
            "foreign(RunningMatchParticipant.team) == 1"
            ")"
        ),
    )


class RunningMatchParticipant(db.Model):
    __tablename__ = "running_match_participant"
    id = Column(Integer, autoincrement=True, primary_key=True)

    match_id = Column(Integer, ForeignKey("running_match.id"))
    team = Column(Integer, nullable=False)  # 0 = Team1, 1 = Team2

    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship("Player", foreign_keys=[player_id], lazy="joined")

    def __repr__(self) -> str:
        return (
            "<RunningMatchParticipant "
            f"match_id={self.match_id} "
            f"team={self.team} "
            f"name={self.player.username} "
            f"class={self.player.character_class.value}"
            ">"
        )


class FinishedMatch(db.Model):
    __tablename__ = "finished_match"
    id = Column(Integer, autoincrement=True, primary_key=True)

    server = Column(Enum(Server), nullable=False)
    winner = Column(Enum(Winner), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    season = Column(Integer, default=SEASON)

    team_1 = relationship(
        "FinishedMatchParticipant", uselist=True,
        primaryjoin=(
            "and_("
            "foreign(FinishedMatchParticipant.match_id) == FinishedMatch.id,"
            "foreign(FinishedMatchParticipant.team) == 0"
            ")"
        ),
        viewonly=True,
    )

    team_2 = relationship(
        "FinishedMatchParticipant", uselist=True,
        primaryjoin=(
            "and_("
            "foreign(FinishedMatchParticipant.match_id) == FinishedMatch.id,"
            "foreign(FinishedMatchParticipant.team) == 1"
            ")"
        ),
        viewonly=True,
    )


class FinishedMatchParticipant(db.Model):
    __tablename__ = "finished_match_participant"
    id = Column(Integer, autoincrement=True, primary_key=True)

    match_id = Column(Integer, ForeignKey("finished_match.id"))
    team = Column(Integer, nullable=False)  # 0 = Team1, 1 = Team2

    points_before = Column(Integer, nullable=False)
    points_after = Column(Integer, nullable=False)

    player_id = Column(Integer, ForeignKey("player.id"))
    username = Column(String(13), nullable=False)
    character_class = Column(Enum(CharacterClass), nullable=False)
    level_land = Column(Integer, nullable=False)
    level_sea = Column(Integer, nullable=False)


class Moderator(db.Model, UserMixin):
    __tablename__ = "moderator"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(128), nullable=False)
    password = Column(String(2048), nullable=False)


class Log(db.Model):
    __tablename__ = "log"

    index = Column(Integer, autoincrement=True, primary_key=True)

    moderator_id = Column(Integer, ForeignKey("moderator.id"), nullable=False)
    message = Column(String(256), nullable=False)

    date = Column(DateTime, default=datetime.datetime.utcnow)
