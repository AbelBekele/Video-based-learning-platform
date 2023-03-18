import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from . import validator
from . import securities

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

    def set_password(self, passw, commit=False):
        passw_hash = securities.generate_hash(passw)
        self.password = passw_hash
        if commit:
            self.save()
        return True

    def verify_password(self, passw):
        passw_hash = self.password
        verified, _ = securities.verify_hash(passw_hash, passw)
        return verified
    
    @staticmethod
    def create_user(email, password=None):
        queryset = User.objects.filter(email=email)
        if queryset.count() != 0:
            raise Exception("User is already registered")
            
        valid, msg, email = validator.validate_email_(email)
        if not valid:
            raise Exception(f"Invalid email address: {msg}")
        
        obj = User(email=email)
        obj.set_password(password)
        obj.save()
        return obj