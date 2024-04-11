from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from typing import List, Any
from . import router


class UpdateVideoRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    photos: List


@router.patch("/{video_id:str}")
def update_video(
    video_id: str,
    input: UpdateVideoRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    update_result = svc.repository.update_video(video_id, jwt_data.user_id, input.dict())
    if update_result.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)
