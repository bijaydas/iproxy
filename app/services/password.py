from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordService:
    def __init__(self):
        self.ph = PasswordHasher()

    def hash(self, plain_password) -> str:
        return self.ph.hash(plain_password)

    def verify_password(self, hashed_password: str, plain_password: str) -> bool:
        try:
            return self.ph.verify(hashed_password, plain_password)
        except VerifyMismatchError:
            return False
