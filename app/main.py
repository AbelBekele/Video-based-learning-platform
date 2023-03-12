from fastapi import FastAPI

#from . import config

main_app = FastAPI()
#settings = config.get_settings()

@main_app.get("/")
def homepage() :
    return {"hello": "world", "keyspace": settings.keyspace} # json data -> REST API
