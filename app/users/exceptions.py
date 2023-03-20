from fastapi import HTTPException

class LoginRequiredException(HTTPException):
    pass

# class LoginReqiredException(Exception):
#     pass