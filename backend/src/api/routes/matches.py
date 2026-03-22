from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_db, require_user
from src.db.models import User
from src.exceptions import MatchNotFound
from src.schemas.matches import MatchRead, MatchUpdate
from src.services.match_service import get_matches, set_match_result

router = APIRouter(prefix="/rounds")


@router.get("/{round_id}/matches")
async def get_round_matches_route(
    round_id: int,
    session: Session = Depends(get_db),
) -> list[MatchRead]:
    return [
        MatchRead.model_validate(obj) for obj in get_matches(session, round_id=round_id)
    ]


@router.post("/{round_id}/matches/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_round_match_route(
    round_id: int,
    match_id: int,
    data: MatchUpdate,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> None:
    try:
        set_match_result(session, match_id=match_id, result=data.result)
    except MatchNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
