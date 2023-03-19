import pathlib
import json
from fastapi import FastAPI
from fastapi import Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table
from pydantic.error_wrappers import ValidationError
from . import config, database
from .users.models import User
from .users.pydantic_schemas import UserSignupSchema

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

@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    return templates.TemplateResponse("authentication/login.html", {
        "request": request,
    })

@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, 
    email: str=Form(...), 
    password: str=Form(...)):
    print (email, password)
    return templates.TemplateResponse("authentication/login.html", {
        "request": request,
    })

@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return templates.TemplateResponse("authentication/signup.html", {
        "request": request,
    })

@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request, 
    email: str=Form(...), 
    password: str=Form(...),
    password_confirm: str=Form(...)
    ):
    data = {}
    errors = []
    error_str = ""
    try:
        cleaned_data = UserSignupSchema(email=email, password=password,
        password_confirm=password_confirm)
        data = cleaned_data.dict()
    except ValidationError as e:
        error_str = e.json()
    try:
        errors = json.loads(error_str)
    except Exception as e:
        errors = [{"loc": "non_field_error", "msg": "Unknown error"}]

    # cleaned_data = UserSignupSchema(email=email, password=password, 
    # password_confirm=password_confirm)
    # print(cleaned_data.dict())
    return templates.TemplateResponse("authentication/signup.html", {
        "request": request,
        "data": data,
        "errors": errors,
    })

@app.get("/users")
def users_list():
    queryset =  User.objects.all().limit(5)
    return list(queryset)