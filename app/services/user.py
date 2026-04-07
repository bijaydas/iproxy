from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.user import User
from app.schemas.requests.auth import SignUpRequest
from app.services.password import PasswordService
from app.exceptions.auth import EmailAlreadyExists


class UserService:
    password_service: PasswordService

    def __init__(self):
        self.password_service = PasswordService()

    def create(self, payload: SignUpRequest, db: Session):
        try:
            user = User(
                email=payload.email.lower(),
                password=self.password_service.hash(payload.password),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            logger.error(e)
            raise EmailAlreadyExists()
        except Exception as e:
            logger.error(e)
            raise e
