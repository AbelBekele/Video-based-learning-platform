import uuid
from app.config import get_settings
from app.users.models import User 
form app.users.exceptions import InvalidUserIDException
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

settings = get_settings()

from .extractor import extract_video_id,
from .extractor import (
    InvalidYouTubeVideoURLException,
    VideoAlreadyAddedException)

# Uses a keyspace to communicate with database
# Accepts email address and password from user
# Generates user id using UUID for newly inserted user
class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    database_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    url = columns.Text()
    host_service = columns.Text(default="youtube")
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(host_id={self.host_id}, host_service={self.host_service})"

    @staticmethod
    def add_video(url, user_id=None):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYouTubeVideoURLException("Invalid YouTube video URL")
        user_exists = User.check_existance(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid User")
        queryset = Video.objects.allow_filtering().filter(host_id=host_id, user_id=user_id)
        if queryset.count() != 0:
            raise VideoAlreadyAddedException("Video is already added")
        return Video.create(host_id=host_id, user_id=user_id, url=url)
