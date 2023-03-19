from pydantic import BaseModel, EmailStr, SecretStr, validator

from .models import User

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr
        
    @validator('email')
    def email_available(cls, v, values, **kwargs):
        queryset = User.objects.filter(email = v)
        if queryset.count() != 0:
            raise ValueError("Email not available")
        return v
        
    @validator("password_confirm")
    def password_matching(cls, v, values, **kwargs):
        password = values.get("password")
        password_confirm = v
        if password != password_confirm:
            raise ValueError("Password do not match")
        return v