import uuid
from typing import Optional
from fastapi import(
    APIRouter,
    Request,
    Form,
    Depends
)
from fastapi.responses import HTMLResponse
from app import utility
from app.shortcuts import render, redirect, find_object
from app.users.decorators import login_required
from app.watchevents.models import WatchEvent
from .pydantic_schemas import VideoCreateSchema
from .models import Video

router = APIRouter(
    prefix = "/videos"
)

def is_htmx(request:Request):
    return request.headers.get("hx-request") == 'true'

@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(
    request: Request, 
    is_htmx=Depends(is_htmx),
    playlist_id:Optional[uuid.UUID]=None
    ):
    print(playlist_id)
    if is_htmx:
        return render(request, "videos/htmx/create.html", {})
    return render(request, "videos/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post_view(request: Request, is_htmx=Depends(is_htmx), title: str = Form(...), url: str = Form(...)):
    raw_data= {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utility.data_or_error_validation_schema(raw_data, VideoCreateSchema)
    redirect_path = data.get('path') or "/videos/create"  
    context = {
        "data": data,
        "errors": errors,
        "title": title,
        "url": url,
    }

    if is_htmx:

        #Handle all HTMX requests
 
        if len(errors) > 0:
            return render(request, "videos/htmx/create.html", context)
        context = {"path": redirect_path, "title": data.get('title')}
        return render(request, "videos/htmx/link.html", context)

    #Handle default HTML requests

    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)
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
    start_time = 0
    if request.user.is_authenticated:
        user_id= request.user.username
        start_time = WatchEvent.get_resume_time(host_id, user_id)
    context = {
        "host_id": host_id,
        "start_time": start_time, 
        "object": obj
    }
    return render(request, "videos/details.html", context)

@router.get("/{host_id}/edit", response_class=HTMLResponse)
@login_required
def video_edit_view(request: Request, host_id: str):
    obj = find_object(Video, host_id=host_id)
    context = {
        "object": obj
    }
    return render(request, "videos/edit.html", context) 



@router.post("/{host_id}/edit", response_class=HTMLResponse)
@login_required
def video_edit_post_view(
        rVideoEditSchemaequest: Request,
          host_id: str, 
        is_htmx=Depends(is_htmx), 
        
        title: str=Form(...), 
        url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    obj = find_object(Video, host_id=host_id)
    data, errors = utility.data_or_error_validation_schema(raw_data, VideoEditSchema)
    if len(errors) > 0:
        return render(request, "videos/edit.html", context, status_code=400)
    obj.title = data.get('title') or obj.title
    obj.update_video_url(url, save=True)
    context = {
        "object": obj
    }
    return render(request, "videos/edit.html", context)



@router.get("/{host_id}/hx-edit", response_class=HTMLResponse)
@login_required
def video_hx_edit_view(
    request: Request, 
    host_id: str, 
    is_htmx=Depends(is_htmx)):
    if not is_htmx:
        raise HTTPException(status_code=400)
    obj = None
    not_found = False
    try:
        obj = find_object(Video, host_id=host_id)
    except:
        not_found = True
    if not_found:
        return HTMLResponse("Not found, please try again.")
    context = {
        "object": obj
    }
    return render(request, "videos/htmx/edit.html", context) 



@router.post("/{host_id}/hx-edit", response_class=HTMLResponse)
@login_required
def video_hx_edit_post_view(
        request: Request,
        host_id: str, 
        is_htmx=Depends(is_htmx), 
        title: str=Form(...), 
        url: str = Form(...),
        delete: Optional[bool] = Form(default=False)):
    if not is_htmx:
        raise HTTPException(status_code=400)
    obj = None
    not_found = False
    try:
        obj = find_object(Video, host_id=host_id)
    except:
        not_found = True
    if not_found:
        return HTMLResponse("Not found, please try again.")
    if delete:
        obj.delete()
        return HTMLResponse('Item Deleted')
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utility.data_or_error_validation_schema(raw_data, VideoEditSchema)
    if len(errors) > 0:
        return render(request, "videos/htmx/edit.html", context, status_code=400)
    obj.title = data.get('title') or obj.title
    obj.update_video_url(url, save=True)
    context = {
        "object": obj
    }
    return render(request, "videos/htmx/list-inline.html", context)

    