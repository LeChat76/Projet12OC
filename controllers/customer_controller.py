from models.customer_model import CustomerModel
from views.customer_view import CustomerView
from constants.constants import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT


class CustomerController:
    """ Customer controller """
    def __init__(self, db):
        self.db = db
        self.customer_view = CustomerView()
        self.customer_model = CustomerModel()

    def menu_customer(self, employee):
        """ Customer menu """
        
        while True:
            choix = self.customer_view.customer_menu()
            if choix == MENU_CUSTOMER_CREATION:
                self.add_customer(employee)
            if choix == MENU_CUSTOMER_UPDATE:
                self.update_customer(employee)
            elif choix == MENU_CUSTOMER_DELETE:
                pass
            elif choix == MENU_CUSTOMER_EXIT:
                break
    
    def add_customer(self, employee):
        """ Method for creation of a new customer """

        new_customer = self.customer_view.add_customer(employee)
        self.customer_model.add_customer(new_customer)
    
    def update_customer(self, employee):
        """ method to update customer """
        
        new_customer = self.customer_view.update_customer(employee)



