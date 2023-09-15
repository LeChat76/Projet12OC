from views.contract_view import ContractView
from models.models import ContractModel, EmployeeModel
from constants.contract import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_SIGNATURE, MENU_CONTRACT_DELETE, MENU_CONTRACT_EXIT
from constants.department import MANAGEMENT
from views.utils_view import display_message, input_message	


class ContractController:
    """ Contract controller """

    def __init__(self, db):
        self.db = db
        self.contract_view = ContractView()
        self.employee_model = EmployeeModel() 
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
        permission = self.employee_model.check_permission_menu(MANAGEMENT, employee_id)
        if permission:
            new_contract_obj = self.contract_view.add_contract(employee_id)
            if new_contract_obj == "q":
                display_message("Ajout de contrat abandonné par l'utilisateur. Retour au menu.", True, True, 3)
            else:
                self.contract_model.add_contract(new_contract_obj)
        else:
            display_message("Vous n'avez pas les authorisations necessaires pour la creation de contrats.\nRetour au menu...", True, True, 3)
    
    def update_contract(self, employee_id):
        """ update contract method """

        # display choice selection (by input or list)
        contract_choice = self.contract_view.select_contract_by_entry()
        if not contract_choice.lower() == "q":
            # if valid choice : convert choice in object
            contract_obj = self.contract_model.create_contract_object(contract_choice)
            if contract_obj:
                #check if contract is signed, if yes, modification is forget
                contract_signed_boolean = self.contract_model.check_signature(contract_obj)
                if not contract_signed_boolean:
                    # check permission to modify contract by the logged employee
                    permission_boolean = self.contract_model.check_permission(employee_id)
                    if permission_boolean:
                        #.... if permit : display customer modification menu
                        self.contract_view.modify_contract(contract_obj)
                    else:
                        #... if not permit : display customer info
                        self.contract_view.display_contract_informations(contract_obj)
                else:
                    self.contract_view.display_contract_informations(contract_obj)
            else:
                display_message("Aucun contrat trouvé avec ce numero. Retour au menu.", True, True, 3)
        else:
            display_message("Retour au menu...", True, True, 3)
    
    def sign_contract(self, employee_id):
        """ sign contract method """

        # check permission to access sign contract menu by the logged employee
        permission_boolean = self.contract_model.check_permission(employee_id)
        if permission_boolean:
            # display choice selection (by input or list)
            contract_choice = self.contract_view.select_contract_by_entry()
            if not contract_choice.lower() == "q":
                # if valid choice : convert choice in object
                contract_obj = self.contract_model.create_contract_object(contract_choice)
                if contract_obj:
                    #check if contract is signed, if yes, modification is forget
                    contract_signed_boolean = self.contract_model.check_signature(contract_obj)
                    if not contract_signed_boolean:
                        self.contract_view.sign_contract(contract_obj)
                    else:
                        display_message("Ce contrat est déjà signé donc interdit de le modifier. Retour au menu...", False, False, 3)
                else:
                    display_message("Aucun contrat trouvé avec ce numero. Retour au menu.", True, True, 3)
            else:
                display_message("Retour au menu...", True, False, 3)
        else:
            display_message("Vous n'êtes pas autorisé à signer des contracts.\nRetour au menu...", True, True, 3)
    
    def delete_contract(self, employee_id):
        """ method to delete contract """

        choice = ""
        # check permission to access to this menu
        permission = self.employee_model.check_permission_menu(MANAGEMENT, employee_id)
        if not permission:
            display_message("Vous n'avez pas la permission de supprimer des contrats. Retour au menu...", True, False, 3)
        else:
            # display choice selection (bye input or list)
            contract_choice = self.contract_view.select_contract_by_entry()
            if not contract_choice.lower() == "q":
                # if valid choice : convert choice in object
                contract_obj = self.contract_model.create_contract_object(contract_choice)
                if contract_obj:
                    #check if contract is signed, if yes, modification is forget
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