from pydantic import BaseModel

class WatchEventSchema(BaseModel):
    host_id: str
    