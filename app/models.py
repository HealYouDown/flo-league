from app.constants import DEFAULT_POINTS
from app.enums import CharacterClassEnum, MatchWinnerEnum, ServerEnum
from app.extensions import db
from app.helpers import get_utc_time

Model = db.Model
Column = db.Column
Integer = db.Integer
String = db.String
Enum = db.Enum
ForeignKey = db.ForeignKey
relationship = db.relationship
DateTime = db.DateTime
Boolean = db.Boolean


class Player(Model):
    __tablename__ = "player"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)    

    server = Column(Enum(ServerEnum), nullable=False)
    name = Column(String, nullable=False)
    guild = Column(String, nullable=True)

    level_land = Column(Integer, nullable=False)
    level_sea = Column(Integer, nullable=False)

    character_class = Column(Enum(CharacterClassEnum), nullable=False)

    points = Column(Integer, nullable=False, default=DEFAULT_POINTS)
    wins = Column(Integer, nullable=False, default=0)
    losses = Column(Integer, nullable=False, default=0)
    draws = Column(Integer, nullable=False, default=0)

    matches = relationship("Match", primaryjoin=(
        "or_(Player.id == Match.p1_id, Player.id == Match.p2_id)"))

    added_on = Column(DateTime, nullable=False, default=get_utc_time)
    updated_on = Column(DateTime, nullable=False, default=get_utc_time)

    def __repr__(self) -> str:
        return (
            f"<Player id={self.id} server={self.server.value} "
            f"name={self.name}>"
        )

    def to_dict(
        self,
        minimal: bool = False,
        ultra_mini: bool = False,
    ) -> dict:
        if ultra_mini:
            return {
                "id": self.id,
                "name": self.name,
                "class": {
                    "key": self.character_class.name,
                    "value": self.character_class.value,
                },
            }

        minimal_dict = {
            "id": self.id,
            "server": {
                "key": self.server.name,
                "value": self.server.value,
            },
            "name": self.name,
            "guild": self.guild,
            "level_land": self.level_land,
            "level_sea": self.level_sea,
            "class": {
                "key": self.character_class.name,
                "value": self.character_class.value,
            },
            "points": self.points,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "matches": [match.to_dict() for match
                        in self.matches]
        }


class ActiveMatch(db.Model):
    __tablename__ = "active_match"
    id = Column(Integer, primary_key=True, autoincrement=True)
    server = Column(Enum(ServerEnum), nullable=False)

    player_1_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player_1 = relationship("Player", foreign_keys=[player_1_id],
                            lazy="joined")

    player_2_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player_2 = relationship("Player", foreign_keys=[player_2_id],
                            lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<ActiveMatch id={self.id} server={self.server.value} "
            f"{self.player_1.name} vs. {self.player_2.name}>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "server": {
                "key": self.server.name,
                "value": self.server.value,
            },
            "player_1": self.player_1.to_dict(minimal=True),
            "player_2": self.player_2.to_dict(minimal=True),
        }


class Match(db.Model):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True, autoincrement=True)
    server = Column(Enum(ServerEnum), nullable=False)
    winner = Column(Enum(MatchWinnerEnum), nullable=False)
    date = Column(DateTime, default=get_utc_time)

    p1_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    p1_name = Column(String, nullable=False)
    p1_level_land = Column(Integer, nullable=False)
    p1_level_sea = Column(Integer, nullable=False)
    p1_character_class = Column(Enum(CharacterClassEnum), nullable=False)
    p1_points = Column(Integer, nullable=False)
    p1_points_change = Column(Integer, nullable=False)

    p2_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    p2_name = Column(String, nullable=False)
    p2_level_land = Column(Integer, nullable=False)
    p2_level_sea = Column(Integer, nullable=False)
    p2_character_class = Column(Enum(CharacterClassEnum), nullable=False)
    p2_points = Column(Integer, nullable=False)
    p2_points_change = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Match id={self.id} server={self.server.value} "
            f"winner={self.winner.name} "
            f"{self.p1_name} vs. {self.p2_name}>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "server": {
                "key": self.server.name,
                "value": self.server.value,
            },
            "winner": {
                "key": self.winner.name,
                "value": self.winner.value,
            },
            "player_1": {
                "id": self.p1_id,
                "name": self.p1_name,
                "level_land": self.p1_level_land,
                "level_sea": self.p1_level_sea,
                "class": {
                    "key": self.p1_character_class.name,
                    "value": self.p1_character_class.value,
                },
                "points": self.p1_points,
                "points_change": self.p1_points_change,
            },
            "player_2": {
                "id": self.p2_id,
                "name": self.p2_name,
                "level_land": self.p2_level_land,
                "level_sea": self.p2_level_sea,
                "class": {
                    "key": self.p2_character_class.name,
                    "value": self.p2_character_class.value,
                },
                "points": self.p2_points,
                "points_change": self.p2_points_change,
            }
        }


class Moderator(db.Model):
    __tablename__ = "moderator"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    admin = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Log(db.Model):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=get_utc_time)
    moderator_id = Column(Integer, ForeignKey("moderator.id"))
    moderator = relationship("Moderator", foreign_keys=[moderator_id])
    message = Column(String)
