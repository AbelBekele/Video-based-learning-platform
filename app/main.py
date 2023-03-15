from fastapi import FastAPI

from cassandra.cqlengine.management import sync_table

from . import config, database
from .users.models import User


app = FastAPI()
DB_SESSION = None
settings = config.get_settings()

@app.on_event("startup")
def on_startup():
    # event is triggred when fastapi starts
    print("Startup Sync")
    DB_SESSION = database.get_session()
    sync_table(User)

@app.get("/")
def homepage() :
    return {"hello": "world", "keyspace": settings.keyspace} # json data -> REST API
@app.get("/users")
def users_list():
    queryset =  User.objects.all().limit(5)
    return list(queryset)