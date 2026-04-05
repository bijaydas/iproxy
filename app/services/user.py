from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.core.logger import logger
from app.models.user import User
from app.schemas.requests.auth import SignUpRequest
from app.services.password import PasswordService
from app.exceptions.auth import EmailAlreadyExists


class UserService:
    password_service: PasswordService

    def __init__(self):
        self.password_service = PasswordService()

    def create(self, payload: SignUpRequest):
        try:
            with SessionLocal() as session:
                user = User(
                    email=payload.email.lower(),
                    password=self.password_service.hash(payload.password),
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
        except IntegrityError as e:
            logger.error(e)
            raise EmailAlreadyExists()
        except Exception as e:
            logger.error(e)
            raise e
