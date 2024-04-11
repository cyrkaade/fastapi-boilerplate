from typing import Any

from fastapi import Depends, UploadFile, File
from pydantic import Field
from typing import List


from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router
from gridfs import GridFS
from bson import ObjectId


class CreateVideoRequest(AppModel):
    name: str
    video: UploadFile

class CreateVideoResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post("/", response_model=CreateVideoResponse)
def create_video(
    name: str,
    video: UploadFile = File(...),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    fs = GridFS(svc.repository.database)
    video_content = video.file.read()
    video_id = fs.put(video_content, filename=name, user_id=ObjectId(jwt_data.user_id))

    return CreateVideoResponse(id=video_id)
