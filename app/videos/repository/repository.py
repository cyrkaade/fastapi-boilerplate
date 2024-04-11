from typing import Any, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult
from bson import ObjectId


class VideoRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_video(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["videos"].insert_one(data)
        return insert_result.inserted_id

    def get_video(self, video_id: str):
        return self.database["videos"].find_one({"_id": ObjectId(video_id)})

    def update_video(self, video_id: str, user_id: str, data: dict[str, Any]) -> UpdateResult:
        return self.database["videos"].update_one(
            filter={"_id": ObjectId(video_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_video(self, video_id: str, user_id: str) -> DeleteResult:
        return self.database["videos"].delete_one(
            {"_id": ObjectId(video_id), "user_id": ObjectId(user_id)}
        )
