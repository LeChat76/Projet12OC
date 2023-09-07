from views.customer import CustomerView
from constants import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT


class CustomerController:
    """ Customer controller """
    def __init__(self):
        self.customer_view = CustomerView()

    def menu_customer(self):
        """ Customer menu """
        while True:
            choix = self.customer_view.player_menu()
            if choix == MENU_CUSTOMER_CREATION:
                self.add_customer()
            if choix == MENU_CUSTOMER_UPDATE:
                pass
            elif choix == MENU_CUSTOMER_DELETE:
                pass
            elif choix == MENU_CUSTOMER_EXIT:
                break
    
    def add_customer(self):
        """ Method for creation of a new customer """
        new_customer = self.customer_view.add_customer()
        print('NEW_CUSTOMER', new_customer)



