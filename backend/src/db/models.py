import typing as t

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.enums import CharacterClass, MatchResult, RoundMode, RoundStatus

from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    is_admin: Mapped[bool] = mapped_column(default=False)

    is_blocked: Mapped[bool] = mapped_column(default=False)


class Player(Base, TimestampMixin):
    """Represents a players character, data is taken from the Game DB."""

    __tablename__ = "player"
    __table_args__ = (Index("ix_player_is_active", "is_active", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str]
    level_land: Mapped[int]
    level_sea: Mapped[int]
    character_class: Mapped[CharacterClass]
    is_female: Mapped[bool]
    is_active: Mapped[bool]


class Season(Base, TimestampMixin):
    """Represents a season."""

    __tablename__ = "season"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    is_running: Mapped[bool] = mapped_column(default=True)

    stats: Mapped[list["PlayerSeasonStats"]] = relationship(
        back_populates="season", cascade="all, delete-orphan"
    )


class PlayerSeasonStats(Base, TimestampMixin):
    __tablename__ = "player_season_stats"

    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), primary_key=True)
    player: Mapped["Player"] = relationship()

    season_id = mapped_column(ForeignKey("season.id"), primary_key=True)
    season: Mapped["Season"] = relationship(back_populates="stats")

    elo: Mapped[int] = mapped_column(default=1000)

    wins: Mapped[int] = mapped_column(default=0)
    losses: Mapped[int] = mapped_column(default=0)
    draws: Mapped[int] = mapped_column(default=0)


class Round(Base, TimestampMixin):
    """Represents an active round, optionally linked to a season."""

    __tablename__ = "round"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    season_id: Mapped[t.Optional[int]] = mapped_column(ForeignKey("season.id"))
    season: Mapped[t.Optional[Season]] = relationship(uselist=False)

    mode: Mapped[RoundMode]

    status: Mapped[RoundStatus] = mapped_column(default=RoundStatus.DRAFT)

    participants: Mapped[list["RoundParticipant"]] = relationship(
        back_populates="round", cascade="all, delete-orphan"
    )

    matches: Mapped[list["RoundMatch"]] = relationship(
        back_populates="round", cascade="all, delete-orphan"
    )


class RoundParticipant(Base, TimestampMixin):
    """Represents a player that is currently added to a round."""

    __tablename__ = "round_participant"

    round_id: Mapped[int] = mapped_column(ForeignKey("round.id"), primary_key=True)
    round: Mapped["Round"] = relationship(back_populates="participants")

    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), primary_key=True)
    player: Mapped["Player"] = relationship()


class RoundMatchParticipant(Base, TimestampMixin):
    """Player that is part of a patch, with its data frozen to the time of match creation."""

    __tablename__ = "round_match_participant"

    id: Mapped[int] = mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("round_match_team.id"))
    team: Mapped["RoundMatchTeam"] = relationship(back_populates="members")

    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))

    # Fields frozen to the time of the match, to have a reliable history
    name: Mapped[str]
    level_land: Mapped[int]
    level_sea: Mapped[int]
    character_class: Mapped[CharacterClass]
    is_female: Mapped[bool]

    elo_before: Mapped[t.Optional[int]]
    elo_change: Mapped[t.Optional[int]]


class RoundMatchTeam(Base, TimestampMixin):
    """Players for a match are always part of a "team", which allows 2v2/3v3/... matchups."""

    __tablename__ = "round_match_team"

    id: Mapped[int] = mapped_column(primary_key=True)

    # match_id: Mapped[int] = mapped_column(ForeignKey("round_match.id"))
    # match: Mapped["RoundMatch"] = relationship(back_populates="teams")

    members: Mapped[list["RoundMatchParticipant"]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )


class RoundMatch(Base, TimestampMixin):
    """Represents a match for a round."""

    __tablename__ = "round_match"

    id: Mapped[int] = mapped_column(primary_key=True)

    round_id: Mapped[int] = mapped_column(ForeignKey("round.id"))
    round: Mapped["Round"] = relationship(back_populates="matches")

    team_1_id: Mapped[int] = mapped_column(ForeignKey("round_match_team.id"))
    team_1: Mapped["RoundMatchTeam"] = relationship(foreign_keys=[team_1_id])

    team_2_id: Mapped[int] = mapped_column(ForeignKey("round_match_team.id"))
    team_2: Mapped["RoundMatchTeam"] = relationship(foreign_keys=[team_2_id])

    match_result: Mapped[MatchResult] = mapped_column(default=MatchResult.UNSET)
