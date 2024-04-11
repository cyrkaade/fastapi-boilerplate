from app.config import database

from .repository.repository import VideoRepository


class Service:
    def __init__(self):
        self.repository = VideoRepository(database)

def get_service():
    svc = Service()
    return svc
