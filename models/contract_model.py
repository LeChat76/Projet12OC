from models.models import Contract
from models.models import Database
from constants.database_config import DB_URL
from views.utils_view import display_message



class ContractModel:
    """ Contract class """

    def __init__(self):
        self.db = Database(DB_URL)
    
    def add_contract(self, new_contract):
        """
        method to add customer in the database
        INPUT : entered values for a new customer
        RESULT : record of the new customer in the database
        """
        
        try:
            session = self.db.get_session()
            session.add(new_contract)
            session.commit()
            display_message("Contrat ajouté avec succès !", True, 2)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de l'ajout du contrat : {str(e)}", True,2 )
            return None
        finally:
            session.close()
