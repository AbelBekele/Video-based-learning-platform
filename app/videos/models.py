import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from . import validator
from . import securities

settings = get_settings()

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
        return f"Video(email={self.email}, user_id={self.user_id})"

    @staticmethod
    def add_video(url, user_id=None):
        pass