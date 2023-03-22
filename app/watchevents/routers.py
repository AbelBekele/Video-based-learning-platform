from fastapi import(
    APIRouter,
    Request
)
from fastapi.responses import HTMLResponse
from .pydantic_schemas import WatchEventSchema
from .models import WatchEvent

router = APIRouter()

@router.post("/api/events/watch", response_model=WatchEventSchema)
def watch_event_view(request:Request, watch_event:WatchEventSchema):
    if (request.user.is_authenticated):
        cleaned_data = watch_event.dict()
        data = cleaned_data.copy()
        data.update({
            "user_id": request.user.username
        })
        WatchEvent.objects.create(**data)
        return cleaned_data
    return cleaned_data