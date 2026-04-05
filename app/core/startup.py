from app.services.setup import ApplicationSetup
from app.core.database import engine

def checks():
    application_setup = ApplicationSetup(engine)

    if not application_setup.is_db_available():
        raise Exception("Database not found")

    missing_tables = application_setup.get_missing_tables()
    if missing_tables:
        raise Exception("Tables not migrated: {}".format(missing_tables))