from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.models import Customer, Contract, Employee, Event
from constants import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

class Database():
    def __init__(self):
        self._session = None

    def connect(self):
        if self._session is None:
            self._session = Session()

    def get_session(self):
        self.connect()
        return self._session

    def create_tables(self):
        db_url = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
        engine = create_engine(db_url)

        Customer.metadata.create_all(engine)
        Contract.metadata.create_all(engine)
        Employee.metadata.create_all(engine)
        Event.metadata.create_all(engine)

        session = self.get_session()
        session.commit()
        session.close()
