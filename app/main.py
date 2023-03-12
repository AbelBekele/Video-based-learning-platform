from fastapi import FastAPI

from cassandra.cqlengine.management import sync_table

from . import config

app = FastAPI()
#settings = config.get_settings()

@app.on_event("startup")
def on_startup():
    # event is triggred when fastapi starts
    print("hello world")

@app.get("/")
def homepage() :
    return {"hello": "world", "keyspace": settings.keyspace} # json data -> REST API
