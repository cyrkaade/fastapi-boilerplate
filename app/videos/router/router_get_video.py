from typing import Any

from fastapi import Depends, Response, UploadFile
from pydantic import Field
from typing import List

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router
from bson import ObjectId
from gridfs import GridFS
from starlette.responses import StreamingResponse


class GetVideoResponse(AppModel):
    id: str
    name: str
    user_id: str

@router.get("/{video_id:str}")
async def get_video(
    video_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> StreamingResponse:
    fs = GridFS(svc.repository.database)
    video_file = fs.get(ObjectId(video_id))
    if not video_file:
        return Response(status_code=404)
    
    async def generate():
        video_content = video_file.read()
        yield video_content
    
    return StreamingResponse(
        content=generate(),
        media_type="video/mp4", 
        headers={
            "Content-Disposition": f'attachment; filename="{video_file.filename}.mp4"',
        }
    )