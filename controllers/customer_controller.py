from models.customer_model import CustomerModel
from views.customer_view import CustomerView
from views.utils_view import display_message, input_message	
from constants.customer import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT


class CustomerController:
    """ Customer controller """

    def __init__(self, db):
        self.db = db
        self.customer_view = CustomerView()
        self.customer_model = CustomerModel(None, None, None, None, None)

    def menu_customer(self, employee_id):
        """ Customer menu """
        
        while True:
            choice = self.customer_view.customer_menu()
            if choice == MENU_CUSTOMER_CREATION:
                self.add_customer(employee_id)
            elif choice == MENU_CUSTOMER_UPDATE:
                self.update_customer(employee_id)
            elif choice == MENU_CUSTOMER_DELETE:
                self.delete_customer(employee_id)
            elif choice == MENU_CUSTOMER_EXIT:
                break
    
    def add_customer(self, employee_id):
        """ creation of customer method """

        # check permission of the logged employee to access to this menu
        permission = self.customer_model.check_permission_customer_menu(employee_id)
        if permission:
            new_customer_tuple = self.customer_view.add_customer()
            new_customer_obj = CustomerModel(
                new_customer_tuple[0],
                new_customer_tuple[1],
                new_customer_tuple[2],
                new_customer_tuple[3],
                employee_id
            )
            self.customer_model.add_customer(new_customer_obj)

        else:
            display_message("Vous n'avez pas les authorisations necessaire pour la creation de clients.\nRetour au menu...", True, True, 3)
    
    def update_customer(self, employee_id):
        """ update customer method """
        
        customers_list = self.customer_model.search_all_customers()
        if customers_list:
            # display choice selection (by input or list)
            customer_choice = self.customer_view.select_customer_by_entry()
            if not customer_choice:
                customer_choice = self.customer_view.select_customer_by_list(customers_list)
            if not customer_choice.lower() == "q":
                # if valid choice : convert choice to object
                customer_obj = self.customer_model.create_customer_object(customer_choice)
                if customer_obj:
                    # check permission to modify customer by the logged employee...
                    permission = self.customer_model.check_permission_customer(employee_id, customer_obj)
                    if permission:
                        #.... if permit : display customer modification menu
                        customer_to_update_obj = self.customer_view.update_customer(customer_obj)
                        if customer_to_update_obj:
                            self.customer_model.update_customer(customer_to_update_obj) 
                        else:
                            display_message("Aucune modification apportée au client, retour au menu.", True, True, 3)
                    else:
                        #... if not permit : display customer info
                        self.customer_view.display_customer_informations(customer_obj)
                else:
                    display_message("Aucun client trouvé avec ce nom. Retour au menu.", True, True, 3)
            else:
                display_message("Retour au menu...", True, True, 3)
        else:
            display_message("Aucun client. Retour au menu...", True, True, 3)

    def delete_customer(self, employee_id):
        """ delete customer method"""

        customers_list = self.customer_model.search_all_customers()
        if customers_list:
            choice = ""
            # check permission to access to this menu
            permission = self.customer_model.check_permission_customer_menu(employee_id)
            if not permission:
                display_message("Vous n'avez pas la permission de supprimer des clients. Retour au menu...", True, False, 3)
            else:
                # display choice selection (bye input or list)
                customer_choice = self.customer_view.select_customer_by_entry()
                if not customer_choice:
                    customers_list = self.customer_model.search_all_customers()
                    customer_choice = self.customer_view.select_customer_by_list(customers_list)
                if not customer_choice.lower() == "q":
                    # if valid choice : convert choice in object
                    customer_obj = self.customer_model.create_customer_object(customer_choice)
                    if customer_obj:
                        while choice.lower() != "o" and choice.lower() != "n":
                            choice = input_message(f"\nEtes vous sure de vouloir supprimer le client '{customer_obj.name}' (o/N)? ")
                            if choice.lower() == "o":
                                self.customer_model.delete_customer(customer_obj)
                                break
                            elif choice.lower() == "n" or choice.lower() == "":
                                display_message("Annulation de la suppression. Retour au menu.", True, True, 3)
                                break
                    else:
                        display_message("Aucun client trouvé avec ce nom. Retour au menu.", True, True, 3)
                else:
                    display_message("Retour au menu...", True, False, 3)
        else:
            display_message("Aucun client. Retour au menu...", True, True, 3)