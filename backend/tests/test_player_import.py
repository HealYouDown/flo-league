from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import Player
from src.services.player_service import update_players_from_csv


def test_import_players(session: Session):
    with open("./tests/artifacts/players1.csv", "rb") as fp:
        data = fp.read()
    update_players_from_csv(session, data=data)

    players = session.scalars(select(Player)).all()
    assert len(players) == 5


def test_update_players(session: Session):
    with open("./tests/artifacts/players1.csv", "rb") as fp:
        data = fp.read()
    update_players_from_csv(session, data=data)

    with open("./tests/artifacts/players2.csv", "rb") as fp:
        data = fp.read()
    update_players_from_csv(session, data=data)

    p = session.scalars(select(Player).where(Player.id == 1)).one()
    assert p.name == "NotJeremy"
    assert p.level_land == 120
