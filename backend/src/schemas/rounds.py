import datetime as dt
import typing as t

from pydantic import BaseModel, ConfigDict

from src.enums import RoundMode, RoundStatus

from .seasons import SeasonRead


class RoundCreate(BaseModel):
    season_id: t.Optional[int]
    name: str
    mode: RoundMode


class RoundRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    mode: RoundMode
    status: RoundStatus

    season: t.Optional[SeasonRead]

    created_at: dt.datetime


class RoundUpdate(BaseModel):
    status: RoundStatus
