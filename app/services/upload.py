import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

import app.constants.log_messages as log_messages
from app.core.logger import logger
from app.core.settings import settings
from app.models import Upload as UploadModel


class UploadService:
    def __init__(self):
        self.allowed_extensions = ["txt", "md"]

    @classmethod
    def get_uniquer_name(cls, extension: str) -> str:
        return f"{uuid.uuid4()}.{extension}"

    def job_description(self, file: UploadFile, user_id: int, db: Session):
        extension = file.filename.split(".")[-1]

        """Verify if the file extension is allowed"""
        if extension not in self.allowed_extensions:
            logger.error(log_messages.UPLOAD_FILE_NOT_ALLOWED.format(
                user_id=user_id,
                filename=file.filename,
                extension=extension,
            ))
            raise Exception(f"{extension} extension not allowed")

        """Upload the file"""
        filename = self.get_uniquer_name(extension)
        filepath = os.path.join(settings.UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as _file:
            shutil.copyfileobj(file.file, _file)

        """Check if there is already a description"""
        description = db.query(UploadModel).filter(UploadModel.user_id == user_id).first()

        if not description:
            description = UploadModel(
                user_id=user_id,
                job_description_path=filepath,
            )
            db.add(description)
            db.commit()
            db.refresh(description)

            return filepath

        description.job_description_path = filepath
        db.add(description)
        db.commit()

        return filepath

    def resume(self, file: UploadFile, user_id: int, db: Session):
        extension = file.filename.split(".")[-1]

        """Verify if the file extension is allowed"""
        if extension not in self.allowed_extensions:
            logger.error(log_messages.UPLOAD_FILE_NOT_ALLOWED.format(
                user_id=user_id,
                filename=file.filename,
                extension=extension,
            ))
            raise Exception(f"{extension} extension not allowed")


        """Upload the file"""
        filename = self.get_uniquer_name(extension)
        filepath = os.path.join(settings.UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as _file:
            shutil.copyfileobj(file.file, _file)

        """Check if there is already a description"""
        description = db.query(UploadModel).filter(UploadModel.user_id == user_id).first()

        if not description:
            description = UploadModel(
                user_id=user_id,
                resume_path=filepath,
            )
            db.add(description)
            db.commit()
            db.refresh(description)

            return filepath

        description.resume_path = filepath
        db.add(description)
        db.commit()

        return filepath
