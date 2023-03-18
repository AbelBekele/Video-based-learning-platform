import pathlib
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table

from . import config, database
from .users.models import User

BASE_DIR = pathlib.Path(__file__).resolve().parent # app/
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DB_SESSION = None
settings = config.get_settings()

@app.on_event("startup")
def on_startup():
    # event is triggred when fastapi starts
    print("Startup Sync")
    DB_SESSION = database.get_session()
    sync_table(User)

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request": request,
        "title" : "Video based learning platform"
    }
    return templates.TemplateResponse("home.html", context)
@app.get("/users")
def users_list():
    queryset =  User.objects.all().limit(5)
    return list(queryset)