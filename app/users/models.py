import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from . import validator
from . import security

settings = get_settings()

class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"

    def set_password(self, pw, commit=False):
        pw_hash = security.generate_hash(pw)
        self.password - pw_hash
        if commit:
            self.save()
        return True

    def verify_password(self, pw):
        pw_hash = self.password
        verified, _ = security.verify_hash(pw_hash, pw)
        return verified
    
    @staticmethod
    def create_user(email, password=None):
        queryset = User.objects.filter(email=email)
        if queryset.count() != 0:
            raise Exception("User is already registered")
            
            validator.validate_email_(email)
            if not valid:
                raise Exception ("Invalid email address: {msg}")
            obj = User(email=email)
            obj.set_password(password)
            obj.save()
            return obj