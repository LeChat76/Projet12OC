from views.contract_view import ContractView
from models.models import ContractModel
from constants.contract_menu import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_DELETE, MENU_CONTRACT_EXIT
from models.utils_model import check_permission_menu, check_permission_customer
from views.utils_view import display_message


class ContractController:
    """ Contract controller """

    def __init__(self, db):
        self.db = db
        self.contract_view = ContractView()
        self.contract_model = ContractModel(None, None, None, None, None) 

    def menu_customer(self, employee):
        """ Contract menu """
        
        while True:
            choix = self.contract_view.contract_menu()
            if choix == MENU_CONTRACT_CREATION:
                self.add_contract(employee)
            if choix == MENU_CONTRACT_UPDATE:
                pass
            elif choix == MENU_CONTRACT_DELETE:
                pass
            elif choix == MENU_CONTRACT_EXIT:
                break
    
    def add_contract(self, employee):
        """ creation of contract method """

        # check permission of the logged employee to access to this menu
        permission = check_permission_menu('management', employee)
        if permission:
            new_contract = self.contract_view.add_contract()
            if new_contract == 'q':
                display_message("Ajout de contrat abandonné par l'utilisateur. Retour au menu.", True, True, 2)
            else:
                self.contract_model.add_contract(new_contract)
        else:
            display_message("Vous n'avez pas les authorisations necessaire pour la creation de clients.", True, True, 2)
    
    def update_contract(self, employee):
        """ update contract method """

        # display choice selection (by input or list)
        contract_choice = self.customer_view.select_contract_by_entry()
        if not contract_choice.lower() == 'q':
            # if valid choice : convert choice in object
            contract = self.customer_model.create_customer_object(contract_choice)
            if contract:
                # check permission to modify customer by the logged employee...
                permission = check_permission_customer(contract, employee)
                if permission:
                    #.... if permit : display customer modification menu
                    self.customer_view.modify_customer(contract)
                else:
                    #... if not permit : display customer info
                    self.customer_view.display_customer_informations(contract)
            else:
                display_message('Aucun contrat trouvé avec ce nom. Retour au menu.', True, True, 2)
        else:
            display_message('Retour au menu...', True, True, 2)