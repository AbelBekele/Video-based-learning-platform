from fastapi import(
    APIRouter,
    Request,
    Form
)
from fastapi.responses import HTMLResponse
from app import utility
from app.shortcuts import render, redirect, find_object
from app.users.decorators import login_required
from .pydantic_schemas import VideoCreateSchema
from .models import Video

router = APIRouter(
    prefix = "/videos"
)

@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request):
    return render(request, "videos/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post_view(request: Request, title: str = Form(...), url: str = Form(...)):
    raw_data= {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utility.data_or_error_validation_schema(raw_data, VideoCreateSchema)
    context = {
        "data": data,
        "errors": errors,
        "url": url
    }
    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)
    redirect_path = data.get('path') or "/videos/create"  
    return redirect(redirect_path)


@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    queryset = Video.objects.all(). limit(100)
    context = {
        "object_list": queryset
    }
    return render(request, "videos/list.html", context)

@router.get("/{host_id}", response_class=HTMLResponse)
def video__view(request: Request, host_id: str):
    obj = find_object(Video, host_id=host_id)
    context = {
        "host_id": host_id,
        "object": obj
    }
    return render(request, "videos/details.html", context)
