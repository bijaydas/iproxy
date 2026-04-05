from pydantic import BaseModel, model_validator


class SignUpRequest(BaseModel):
    email: str
    password: str
    confirm_password: str

    @model_validator(mode="before")
    def validate_passwords(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        return values

class LoginRequest(BaseModel):
    email: str
    password: str