from views.contract_view import ContractView, CustomerView
from models.models import ContractModel, CustomerModel
from constants.contract import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_SIGNATURE, MENU_CONTRACT_DELETE, MENU_CONTRACT_EXIT
from views.utils_view import display_message, input_message	


class ContractController:
    """ Contract controller """

    def __init__(self, db):
        self.db = db
        self.contract_view = ContractView()
        self.customer_view = CustomerView()
        self.customer_model = CustomerModel(None, None, None, None, None)
        self.contract_model = ContractModel(None, None, None, None, None, None) 

    def menu_customer(self, employee_id):
        """ Contract menu """
        
        while True:
            choice = self.contract_view.contract_menu()
            if choice == MENU_CONTRACT_CREATION:
                self.add_contract(employee_id)
            elif choice == MENU_CONTRACT_UPDATE:
                self.update_contract(employee_id)
            elif choice == MENU_CONTRACT_SIGNATURE:
                self.sign_contract(employee_id)
            elif choice == MENU_CONTRACT_DELETE:
                self.delete_contract(employee_id)
            elif choice == MENU_CONTRACT_EXIT:
                break
    
    def add_contract(self, employee_id):
        """ creation of contract method """

        # check permission of the logged employee to access to this menu
        permission = self.contract_model.check_permission(employee_id)
        if permission:
            new_contract_values = self.contract_view.add_contract()
            customer_name = self.customer_view.select_customer_by_entry()
            if not customer_name:
                customers_list = self.customer_model.search_all_customers()
                customer_choice = self.customer_view.select_customer_by_list(customers_list)
                customer_obj = self.customer_model.create_customer_object(customer_choice)
            else:
                customer_obj = self.customer_model.create_customer_object(customer_name)
            customer_info = new_contract_values[0]
            price = new_contract_values[1]
            due = new_contract_values[2]
            status = new_contract_values[3]
            new_contract_obj = ContractModel(customer_info, price, due, status, customer_obj, employee_id)
            self.contract_model.add_contract(new_contract_obj)
        else:
            display_message("Vous n'êtes pas autorisé à créer des contrats. Retour au menu...", True, True, 3)
    
    def delete_contract(self, employee_id):
        """ method to delete contract """

        # check permission to access to this menu
        permission = self.contract_model.check_permission(employee_id)
        if not permission:
            display_message("Vous n'avez pas la permission de supprimer des contrats. Retour au menu...", True, False, 3)
        else:
            # display choice selection (bye input or list)
            contract_choice = self.contract_view.select_contract_by_entry()
            if not contract_choice:
                contracts_list = self.contract_model.search_all_contracts()
                contract_choice = self.contract_view.select_contract_by_list(contracts_list)
            if not contract_choice.lower() == "q":
                # if valid choice : convert choice in object
                contract_obj = self.contract_model.create_contract_object(contract_choice)
                if contract_obj:
                    #check if contract is signed, if yes, deletion is forbidden
                    contract_signed_boolean = self.contract_model.check_signature(contract_obj)
                    if contract_signed_boolean:
                        display_message("Ce contrat est signé, interdit de le supprimer. Retour au menu...", True, False, 3)
                    else:
                        while choice.lower() != "o" and choice.lower() != "n":
                            choice = input_message(f"\nEtes vous sure de vouloir supprimer le contrat '{contract_obj.id} (o/N)? ")
                            if choice.lower() == "o":
                                self.contract_model.delete_contract(contract_obj)
                            elif choice.lower() == "n" or choice.lower() == "":
                                display_message("Annulation de la suppression. Retour au menu.", True, True, 3)
                                break
                else:
                    display_message("Aucun contrat trouvé avec ce nom. Retour au menu.", True, True, 3)
            else:
                display_message("Retour au menu...", True, False, 3)
    
    def update_contract(self, employee_id):
        """ update contract method """

        # display choice selection (by input or list)
        contract_choice = self.contract_view.select_contract_by_entry()
        if contract_choice:
            check_if_contract_exists_boolean = self.contract_model.check_if_contract_exists(contract_choice)
            if not check_if_contract_exists_boolean:
                display_message("Ce numéro de contrat n'est pas repertorié dans la base de donnée.\nVeuillez choisir dans la liste des contrats non signés.", False, True, 2)
                contracts_list = self.contract_model.search_all_contracts()
                contract_choice = self.contract_view.select_contract_by_list(contracts_list)
        elif not contract_choice:
            contracts_list = self.contract_model.search_all_contracts()
            contract_choice = self.contract_view.select_contract_by_list(contracts_list)
        if not contract_choice.lower() == "q":
            # if valid choice : convert choice to object
            contract_obj = self.contract_model.create_contract_object(contract_choice)
            if contract_obj:
                # check permission to modify customer by the logged employee...
                permission = self.contract_model.check_permission(employee_id)
                contract_signed_boolean = self.contract_model.check_signature(contract_obj)
                if permission:
                    if not contract_signed_boolean:
                        #.... if permit : display contract modification menu
                        contract_to_update_obj = self.contract_view.update_contract(contract_obj)
                        if contract_to_update_obj:
                            self.contract_model.update_contract(contract_to_update_obj)
                        else:
                            display_message("Aucune modification apportée au contrat, retour au menu.", True, True, 3)
                    else:
                        display_message("Ce contrat est déjà signé, interdit de le modifier", True, True, 0)
                        self.contract_view.display_contract_informations(contract_obj)
                else:
                        #... if not permit : display contract info
                        self.contract_view.display_contract_informations(contract_obj)
        else:
            display_message("Modification d'un contrat abandonnée. Retour au menu...", True, True, 3) 
        
    def sign_contract(self, employee_id):
        """ method to sign contract """

        choice = ""
        # check permission to access to this menu
        permission = self.contract_model.check_permission(employee_id)
        if not permission:
            display_message("Vous n'avez pas la permission de signer des contrats. Retour au menu...", True, False, 3)
        else:
            not_signed_contracts_list = self.contract_model.select_not_signed_contract()
            if not_signed_contracts_list:
                # display choice selection (bye input or list)
                contract_choice = self.contract_view.select_contract_by_entry()
                if contract_choice:
                    check_if_contract_exists_boolean = self.contract_model.check_if_contract_exists(contract_choice)
                    if not check_if_contract_exists_boolean:
                        display_message("Ce numéro de contrat n'est pas repertorié dans la base de donnée.\nVeuillez choisir dans la liste des contrats non signés.", True, True, 2)
                        contract_choice = self.contract_view.select_contract_by_list(not_signed_contracts_list)
                elif not contract_choice:
                    not_signed_contracts_list = self.contract_model.select_not_signed_contract()
                    contract_choice = self.contract_view.select_contract_by_list(not_signed_contracts_list)
                if not contract_choice.lower() == "q":
                    # if valid choice : convert choice in object
                    contract_obj = self.contract_model.create_contract_object(contract_choice)
                    check_if_contract_signed_boolean = self.contract_model.check_signature(contract_obj)
                    if check_if_contract_signed_boolean:
                        display_message("Ce contrat est déjà signé. Retour au menu...", True, True, 3)
                    else:
                        while choice.lower() != "o" and choice.lower() != "n":
                            choice = input_message(f"\nEtes vous sure de vouloir signer le contrat {contract_obj.id} (o/N)? ")
                            if choice.lower() == "o":
                                self.contract_model.sign_contract(contract_obj)
                                display_message(f"Contrat numéro {contract_obj.id} signé. Retour au menu...", True, True, 3)
                            elif choice.lower() == "n" or choice.lower() == "":
                                display_message("Annulation de la signature. Retour au menu.", True, True, 3)
                                break
                else:
                    display_message("Annulation de la signature. Retour au menu.", True, True, 3)
            elif not not_signed_contracts_list:
                display_message("Plus aucun contrat à signer. Retour au menu...", True, True, 3)
