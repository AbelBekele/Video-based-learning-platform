from fastapi import(
    APIRouter,
    Request
)
from fastapi.responses import HTMLResponse
from app.shortcuts import render, redirect

router = APIRouter(
    prefix = "/videos"
)

@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    return render(request, "videos/list.html", {})

@router.get("/details", response_class=HTMLResponse)
def video__view(request: Request):
    return render(request, "videos/details.html", {})
