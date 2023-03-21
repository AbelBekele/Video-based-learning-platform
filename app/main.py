import pathlib
import json
from fastapi import FastAPI
from fastapi import Request
from fastapi import Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from cassandra.cqlengine.management import sync_table
from pydantic.error_wrappers import ValidationError
from . import config, database, utility
from .shortcuts import render, redirect
from .users.models import User
from .users.decorators import login_required
from .users.pydantic_schemas import UserSignupSchema
from .users.pydantic_schemas import UserLoginSchema
from .users.backends import JWTCookieBackend
from .videos.models import Video
from .videos.routers import router as video_router
from .watchevents.models import WatchEvent

BASE_DIR = pathlib.Path(__file__).resolve().parent # app/

# could be removed if decided to use render totally
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(video_router)

# could be removed if decided to use render totally
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DB_SESSION = None
settings = config.get_settings()

from .handlers import * #noqa

@app.on_event("startup")
def on_startup():
    # event is triggred when fastapi starts
    print("Startup Sync")
    DB_SESSION = database.get_session()
    sync_table(User)
    sync_table(Video)
    sync_table(WatchEvent)

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {}, status_code=200)
    return render(request, "home.html", {})

@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request):
    context = {}
    return render(request, "account.html", context)

@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get("session_id") or None
    return render(request, "authentication/login.html", 
    {"logged_in": session_id is not None})
  
@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, 
    email: str=Form(...), 
    password: str=Form(...)):
    raw_data = {
        "email": email,
        "password": password,
    }
    data, errors = utility.data_or_error_validation_schema(raw_data, UserLoginSchema)
    context = {
                "data": data,
                "errors": errors,
            }
    if len(errors) > 0:
        return render(request, "authentication/login.html", context, status_code=400)

    #print(data)
    return redirect("/", cookies=data)

@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "authentication/signup.html", {
    })

@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request, 
    email: str=Form(...), 
    password: str=Form(...),
    password_confirm: str=Form(...)
    ):
    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data, errors = utility.data_or_error_validation_schema(raw_data, UserSignupSchema)
    return redirect("/login", cookies=data)

@app.get("/users")
def users_list():
    queryset =  User.objects.all().limit(5)
    return list(queryset)

@app.post("/watch-event")
def watch_event_view(request:Request, data:dict):
    print("data", data)
    if (request.user.is_authenticated):
        WatchEvent.objects.create(
            host_id = data.get("videoId"),
            user_id = request.user.username,
            start_time= 0,
            duration = 500,
            end_time = data.get("currentTime"),
            complete= False            
        )
    return{"working": True}