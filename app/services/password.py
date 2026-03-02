from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordService:
    def __init__(self):
        self.ph = PasswordHasher()

    def hash(self, plain_password) -> str:
        return self.ph.hash(plain_password)

    def verify_password(self, hashed_password) -> bool:
        try:
            self.ph.verify(hashed_password)
            return True
        except VerifyMismatchError:
            return False
