import time
from models.models import Database
from constants.constants import DB_URL


class CustomerModel:
    """ Customer class """

    def __init__(self):
        self.db = Database(DB_URL)

    def search_customer(self):
        """ method to search customer in the database """

        pass

    def add_customer(self, new_customer):
        """
        method to add customer in the database
        INPUT : entered values for a new customer
        OUTPUT : record of the new customer in the database
        """
        
        try:
            session = self.db.get_session()
            session.add(new_customer)
            session.commit()
            print("Client ajouté avec succès !")
            time.sleep(1)
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'ajout du client : {str(e)}")
            time.sleep(1)
            return None
        finally:
            session.close()

