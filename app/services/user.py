from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.exceptions.auth import EmailAlreadyExists, InvalidPassword, InvalidUser
from app.models import Session as SessionModel
from app.models import User
from app.schemas.requests.auth import LoginRequest, SignUpRequest
from app.services.jwt import JWTService
from app.services.password import PasswordService


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
