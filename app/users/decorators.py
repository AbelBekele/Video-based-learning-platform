from fastapi import Request
from functools import wraps
from .auth import verify_user_id
from .exceptions import LoginRequiredException

def login_required(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise LoginRequiredException(status_code=401)
        return func(request, *args, **kwargs)
    return wrapper
    