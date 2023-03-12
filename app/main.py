from fastapi import FastAPI

main_app = FastAPI()

@main_app.get("/")
def homepage() :
    return {"hello": "world"} # json data -> REST API
