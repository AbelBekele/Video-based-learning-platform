import 
from cassandra.cassandra import columns
from cassandra.cqlengine.models import Model


class User(Model):
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"