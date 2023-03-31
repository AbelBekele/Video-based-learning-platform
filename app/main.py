import pathlib
import json
from typing import Optional
from fastapi import FastAPI
from fastapi import Request
from fastapi import Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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
from .watchevents.pydantic_schemas import WatchEventSchema
from .watchevents.routers import router as watch_event_router
from .playlists.routers import router as playlist_router

BASE_DIR = pathlib.Path(__file__).resolve().parent # app/

# could be removed if decided to use render totally
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR/"templates/static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(video_router)
app.include_router(watch_event_router)
app.include_router(playlist_router)

# could be removed if decided to use render totally
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DB_SESSION = None
settings = config.get_settings()

from .handlers import * #noqa

@app.get("/healthcheck")
def read_root():
     return {"status": "ok"}

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
        context = {"image_path": "/static/assets/img.svg"}
        return render(request, "dashboard.html", context, status_code=200)
    return render(request, "home.html", {})

@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request):
    context = {}
    return render(request, "account.html", context)

@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    return render(request, "authentication/login.html", 
    {})
  
@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, 
    email: str=Form(...), 
    password: str=Form(...),
    next: Optional[str] = "/"
    ):
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
    if "http://127.0.0.1" not in next:
        next = '/'
    return redirect(next, cookies=data)


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
    context = {
                "data": data,
                "errors": errors,
            }
    if len(errors) > 0:
        return render(request, "authentication/signup.html", context, status_code=400)
    else:
        User.create_user(email, password_confirm)  
    return redirect("/login", cookies=data)

@app.get("/users")
def users_list():
    queryset =  User.objects.all().limit(5)
    return list(queryset)

@app.get("/logout", response_class=HTMLResponse)
def logout_get_view(request: Request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, "authentication/logout.html", {})

@app.post("/logout", response_class=HTMLResponse)
def logout_post_view(request: Request):
    return redirect("/login", remove_session=True)