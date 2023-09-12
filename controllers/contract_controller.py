from views.contract_view import ContractView
from models.contract_model import ContractModel
from constants.contract_menu import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_DELETE, MENU_CONTRACT_EXIT


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
                pass
            if choix == MENU_CONTRACT_UPDATE:
                pass
            elif choix == MENU_CONTRACT_DELETE:
                pass
            elif choix == MENU_CONTRACT_EXIT:
                break