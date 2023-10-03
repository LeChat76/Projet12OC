from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.utils_view import display_message
# import bcrypt

Base = declarative_base()


class DatabaseModel:
    """Database class"""

    def __init__(self, DB_URL_ADMIN):
        self.engine = create_engine(DB_URL_ADMIN)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """method to create tables + superadmin account"""
        try:
            session = self.Session()
            Base.metadata.create_all(self.engine)
        except Exception as e:
            display_message(
                f"Probleme lors de la creation des bases de données : {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()

    def tables_exist(self):
        """ method to check if tables already exists """

        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        required_tables = ["customer", "employee", "contract", "event"]
        return all(table_name in table_names for table_name in required_tables)

    def get_session(self):
        return self.Session()
