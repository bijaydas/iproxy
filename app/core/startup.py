import os
from app.core.database import engine
from app.services.setup import ApplicationSetup
from app.core.settings import settings


def checks():
    application_setup = ApplicationSetup(engine)

    if not application_setup.is_db_available():
        raise Exception("Database not found")

    missing_tables = application_setup.get_missing_tables()
    if missing_tables:
        raise Exception("Tables not migrated: {}".format(missing_tables))

    application_setup.setup_folders()

    os.environ["LANGSMITH_TRACING"] = settings.LANGSMITH_TRACING
    os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
