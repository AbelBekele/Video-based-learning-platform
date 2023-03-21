from fastapi import HTTPException

class LoginRequiredException(HTTPException):
    pass

# class LoginReqiredException(Exception):
#     pass

class UserHasAccountException(Exception):
    """User already has account."""


class InvalidEmailException(Exception):
    """Invalid email address"""

class InvalidUserIDException(Exception):
    """Invalid user id"""