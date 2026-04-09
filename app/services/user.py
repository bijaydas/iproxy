from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.exceptions.auth import EmailAlreadyExists, InvalidPassword, InvalidUser
from app.models import Session as SessionModel
from app.models import User
from app.schemas.requests.auth import LoginRequest, SignUpRequest
from app.services.jwt import JWTService
from app.services.password import PasswordService
from app.enums import UserStatus
from app.utils.general import pprint


class UserService:
    password_service: PasswordService

    def __init__(self):
        self.password_service = PasswordService()
        self.jwt_service = JWTService()

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

    def login(self, payload: LoginRequest, db: Session):
        user = db.query(User).filter(User.email == payload.email).first()

        if not user:
            raise InvalidUser()

        ok_password = self.password_service.verify_password(
            str(user.password),
            payload.password,
        )
        if not ok_password:
            raise InvalidPassword()

        output = {
            "email": user.email,
        }

        jwt_token = self.jwt_service.create_access_token(str(user.id),{"email": user.email})
        output["token"] = jwt_token

        session_model = SessionModel(
            user_id=user.id,
            jwt_token=jwt_token,
        )

        db.add(session_model)
        db.commit()
        db.refresh(session_model)

        return output

    @staticmethod
    def get_profile(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise InvalidUser()

        return user

    @staticmethod
    def is_active(user: User):
        return user.status == UserStatus.active.value

    @staticmethod
    def logout(user_id: str, token: str, db: Session):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.error(f"User with id {user_id} does not exist")
            raise InvalidUser()

        current_session = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.jwt_token == token,
            SessionModel.logged_out_at.is_(None),
        ).first()

        if not current_session:
            logger.error(f"User with id {user_id} does not exist")
            raise InvalidUser()

        current_session.logged_out_at = datetime.now()
        db.commit()
        db.refresh(current_session)

        return True

    @staticmethod
    def is_logged_in(user_id: str, token: str, db: Session):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.error(f"User with id {user_id} does not exist")
            raise InvalidUser()

        current_session = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.jwt_token == token,
            SessionModel.logged_out_at.is_(None),
        ).first()

        if not current_session:
            logger.error(f"User with id {user_id} does not exist")
            raise InvalidUser()

        return True