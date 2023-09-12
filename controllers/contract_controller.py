from views.contract_view import ContractView
from models.contract_model import ContractModel
from constants.contract_menu import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_DELETE, MENU_CONTRACT_EXIT
from models.utils_model import check_permission_menu
from views.utils_view import display_message


class ContractController:
    """ Contract controller """

    def __init__(self, db):
        self.db = db
        self.contract_view = ContractView()
        self.contract_model = ContractModel() 

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
            new_contract = self.contract_view.add_contract(employee)
            if new_contract == 'q':
                display_message("Ajout de contrat abandonné par l'utilisateur. Retour au menu.", True, 2)
            else:
                self.contract_model.add_contract(new_contract)
        else:
            display_message("Vous n'avez pas les authorisations necessaire pour la creation de clients.", True, 2)
    
    def update_contract(self, employee):
        """ update contract method """

        pass