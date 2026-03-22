from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from src.api.deps import get_db, require_admin, require_user
from src.db.models import User
from src.schemas.players import PlayerRead
from src.services.player_service import search_players, update_players_from_csv

router = APIRouter(prefix="/players")


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_players_route(
    file: UploadFile,
    user: User = Depends(require_admin),
    session: Session = Depends(get_db),
):
    content = await file.read()

    try:
        update_players_from_csv(session, data=content)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.get("/")
async def search_players_route(
    name: str = Query(..., min_length=1),
    limit: int = Query(20, le=100),
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> list[PlayerRead]:
    return [
        PlayerRead.model_validate(obj)
        for obj in search_players(session, name=name, limit=limit)
    ]
