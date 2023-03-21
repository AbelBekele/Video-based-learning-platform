from pydantic import BaseModel, validator, root_validator
from .extractor import extract_video_id
from app.users.exceptions import InvalidUserIDException
from .exceptions import (
    InvalidYouTubeVideoURLException,
    VideoAlreadyAddedException)
from .models import Video

class VideoCreateSchema(BaseModel):
    url: str
    user_id: str

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid URL")
        retrun url

    @root_validator
    def validate_data(cls, values):
        url = values.get("url")
        user_id = valuse.get("user_id")
        video_obj = None
        try:
            video_obj = Video.add_vidoe(url, user_id=user_id)
        except InvalidYouTubeVideoURLException:
            raise ValueError(f"{url} is not a valid YouTube URL")
        except VideoAlreadyAddedException:
            raise ValueError(f"{url} has already been added to your account.")
        except InvalidUserIDException:
            raise ValueError("There's a problem with your account, please check your account and try again.")
        except ValueError:
            raise ValueError("There is a problem with your account, Please check your account and try again")
        if video_obj is None:
            raise ValueError("There is a problem with your account, Please check your account and try again")
        if not isinstance(video_obj, Video):
            raise ValueError("There is a problem with your account, Please check your account and try again")
        retrun video_obj.dict()