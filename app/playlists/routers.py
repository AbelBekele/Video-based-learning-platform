import uuid
from starlette.exceptions import HTTPException
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from app import utility
from app.users.decorators import login_required
from app.shortcuts import render, redirect, find_object, is_htmx

from app.watchevents.models import WatchEvent
from .models import Playlist
from .pydantic_schemas import PlaylistCreateSchema, PlaylistVideoAddSchema


router = APIRouter(
    prefix='/playlists'
) 


@router.get("/create", response_class=HTMLResponse)
@login_required
def playlist_create_view(request: Request):
    return render(request, "playlists/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def playlist_create_post_view(request: Request, title: str=Form(...)):
    raw_data = {
        "title": title,
        "user_id": request.user.username
    }
    data, errors = utility.data_or_error_validation_schema(raw_data, PlaylistCreateSchema)
    context = {
        "data": data,
        "errors": errors,
    }
    if len(errors) > 0:
        return render(request, "playlists/create.html", context, status_code=400)
    obj = Playlist.objects.create(**data)
    redirect_path = obj.path or "/playlists/create" 
    return redirect(redirect_path)


@router.get("/", response_class=HTMLResponse)
def playlist_list_view(request: Request):
    queryset = Playlist.objects.all().limit(100)
    context = {
        "object_list": queryset
    }
    return render(request, "playlists/list.html", context)

# host_id='playlist-1'
# f"{host_id} is cool"

@router.get("/{db_id}", response_class=HTMLResponse)
def playlist_detail_view(request: Request, db_id: str):
    obj = find_object(Playlist, db_id=db_id)
    if request.user.is_authenticated:
        user_id = request.user.username
    context = {
        "object": obj,
        "videos": obj.get_videos(),
    }
    return render(request, "playlists/details.html", context) 

@router.get("/{db_id}/add-video", response_class=HTMLResponse)
@login_required
def playlist_video_add_view(
    request: Request, 
    db_id: uuid.UUID,
    is_htmx=Depends(is_htmx),
    ):
    context = {"db_id": db_id}
    if not is_htmx:
        raise HTTPException(status_code=400)
    return render(request, "playlists/htmx/add-video.html", context)
    


@router.post("/{db_id}/add-video", response_class=HTMLResponse)
@login_required
def playlist_video_add_post_view(
    request: Request,
    db_id: uuid.UUID,
    is_htmx=Depends(is_htmx), 
    title: str=Form(...), 
    url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username,
        "playlist_id": db_id
    }
    data, errors = utility.data_or_error_validation_schema(raw_data, PlaylistVideoAddSchema)
    redirect_path = data.get('path') or f"/playlists/{db_id}" 
    
    context = {
        "data": data,
        "errors": errors,
        "title": title,
        "url": url,
        "db_id": db_id,
    }

    if not is_htmx:
        raise HTTPException(status_code=400)

    #Handle all HTMX requests

    if len(errors) > 0:
        return render(request, "playlists/htmx/add-video.html", context)
    context = {"path": redirect_path, "title": data.get('title')}
    return render(request, "videos/htmx/link.html", context)