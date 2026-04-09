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

class ResetPasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode="before")
    def validate_password(cls, values):
        current_password = values.get("current_password")
        new_password = values.get("new_password")
        confirm_password = values.get("confirm_password")

        if current_password == new_password:
            raise ValueError("Old and new password cannot be the same")

        if new_password != confirm_password:
            raise ValueError("Passwords do not match")

        if len(current_password) < 6:
            raise ValueError("Password must be at least 6 characters")

        return values
