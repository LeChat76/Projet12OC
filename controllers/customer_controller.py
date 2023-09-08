import time
from views.utils_view import clear_screen
from views.customer_view import CustomerView
from constants import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT


class CustomerController:
    """ Customer controller """
    def __init__(self, db):
        self.customer_view = CustomerView()
        self.db = db

    def menu_customer(self, employee_id):
        """ Customer menu """
        while True:
            choix = self.customer_view.customer_menu()
            if choix == MENU_CUSTOMER_CREATION:
                self.add_customer(employee_id)
            if choix == MENU_CUSTOMER_UPDATE:
                pass
            elif choix == MENU_CUSTOMER_DELETE:
                pass
            elif choix == MENU_CUSTOMER_EXIT:
                break
    
    def add_customer(self, employee_id):
        """ Method for creation of a new customer """
        new_customer = self.customer_view.add_customer(employee_id)
        
        try:
            session = self.db.get_session()
            session.add(new_customer)
            session.commit()
            session.close()
            clear_screen()
            print("Client ajouté avec succès !")
            time.sleep(1)

        except Exception as e:
            print(f"Erreur lors de l'ajout du client : {str(e)}")
            input()
            return None



