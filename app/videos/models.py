import uuid
from app.config import get_settings
from app.users.models import User 
from app.users.exceptions import InvalidUserIDException
from app.shortcuts import templates
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

settings = get_settings()

from .extractor import extract_video_id
from .exceptions import (
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
    title = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(title={self.title}, host_id={self.host_id}, host_service={self.host_service})"
    
    def render(self):
        basename = self.host_service # youtube, vimeo
        template_name = f"videos/renderers/{basename}.html"
        context = {"host_id": self.host_id}
        t = templates.get_template(template_name)
        return t.render(context)

    def as_data(self):
        return {f"{self.host_service}_id": self.host_id, "path": self.path, "title": self.title}

    @property
    def path(self):
        return f"/videos/{self.host_id}"

    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYouTubeVideoURLException("Invalid YouTube video URL")
        user_exists = User.check_existance(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid User")
        queryset = Video.objects.allow_filtering().filter(host_id=host_id)#, user_id=user_id)
        if queryset.count() != 0:
            raise VideoAlreadyAddedException("Video is already added")
        return Video.create(host_id=host_id, user_id=user_id, url=url, **kwargs)