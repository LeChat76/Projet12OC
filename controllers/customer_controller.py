import time
from models.customer_model import CustomerModel
from views.customer_view import CustomerView
from models.utils_model import check_permission_menu, check_permission_customer
from views.utils_view import display_message, input_message	
from constants.customer_menu import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT


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
                self.delete_customer(employee)
            elif choix == MENU_CUSTOMER_EXIT:
                break
    
    def add_customer(self, employee):
        """ Method for creation of a new customer """

        permission = check_permission_menu('commercial', employee)
        if permission:
            new_customer = self.customer_view.add_customer(employee)
            self.customer_model.add_customer(new_customer)
        else:
            display_message("Vous n'avez pas les authorisations necessaire pour la creation de clients.", True, 2)
    
    def update_customer(self, employee):
        """ method to update customer """
        
        customer_choice = self.customer_view.select_customer(employee)
        customer = self.customer_model.select_customer(customer_choice)
        if customer:
            permission = check_permission_customer(customer, employee)
            self.customer_view.modify_customer(customer_choice, permission)
        else:
            display_message('Aucun client trouvé avec ce nom. Retour au menu.', True, 2)
    
    def delete_customer(self, employee):
        """ method tu delete customer """

        permission = check_permission_menu('commercial', employee)
        if not permission:
            print("Vous n'avez pas la permission de suppression des clients.")
            time.sleep(2)
        else:
            customer_choice = self.customer_view.select_customer(employee)
            customer = self.customer_model.select_customer(customer_choice)
            if customer:
                answer = input_message(f'Etes vous sure de vouloir supprimer le client "{customer.name}" (o/N)? ')
                if answer.lower() == 'o':
                    self.customer_model.delete_customer(customer)
                else:
                    display_message('Annulation de la suppression. Retour au menu.', True, 2)
            else:
                display_message('Aucun client trouvé avec ce nom. Retour au menu.', True, 2)





