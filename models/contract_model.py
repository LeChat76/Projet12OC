from models.models import Contract
from models.models import Database
from constants.database_config import DB_URL



class ContractModel:
    """ Contract class """

    def __init__(self):
        self.db = Database(DB_URL)
