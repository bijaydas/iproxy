from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import engine


class ApplicationSetup:
    def __init__(self, db_engine: Engine = engine, required_tables: list[str] | None = None):
        self.db_engine = db_engine
        self.required_tables = required_tables or ["users"]

    def is_db_available(self) -> bool:
        try:
            with self.db_engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False

    def get_missing_tables(self) -> list[str]:
        inspector = inspect(self.db_engine)
        existing_tables = set(inspector.get_table_names())
        return [table_name for table_name in self.required_tables if table_name not in existing_tables]
