import datetime as dt
import typing as t

from pydantic import BaseModel, ConfigDict

from .players import PlayerRead


class SeasonCreate(BaseModel):
    name: str
    description: str


class SeasonUpdate(BaseModel):
    name: t.Optional[str]
    description: t.Optional[str]
    is_running: t.Optional[bool]


class SeasonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    is_running: bool
    created_at: dt.datetime


class SeasonPlayerStatsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    season: SeasonRead
    player: PlayerRead

    elo: int
    wins: int
    losses: int
    draws: int
