import datetime
from jose import jwt, ExpiredSignatureError
from .models import User
from app import config

settings = config.get_settings()

# Step 1 autenticating user first
def authenticate(email, password):
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None
    if not user_obj.verify_password(password):
        return None
    return user_obj

# Step 2 logging in after autenticating
def login(user_obj, expires = 5):
    raw_data = {
    "user_id": f"{user_obj.user_id}",
    "role" : "admin",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)
}
    return jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algorithm)

# Step verifying the token of the user
def verify_user_id(token):
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=(settings.jwt_algorithm))
    except ExpiredSignatureError as e:
        print(f"{e} so you have been logged out")
    except:
        pass
    if 'user_id' not in data:
        return None
    return data