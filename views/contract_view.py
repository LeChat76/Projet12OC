from views.utils_view import clear_screen
from models.models import Contract
from constants.contract_menu import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_DELETE, MENU_CONTRACT_EXIT


class ContractView:
    """ Customer view class """

    def __init__(self):
        self.contract_model = Contract()

    def contract_menu(self):
        """ Menu 2 - CONTRAT """

        choice = None
        while choice !=  MENU_CONTRACT_CREATION and choice != MENU_CONTRACT_UPDATE and\
            choice != MENU_CONTRACT_DELETE and choice != MENU_CONTRACT_EXIT:
            clear_screen()
            print("+-------------------------------+")
            print("|          MENU CONTRAT         |")
            print("+-------------------------------+")
            print("| 1 - création d'un contrat     |")
            print("| 2 - voir/modifier un contrat  |")
            print("| 3 - suppression d'un contrat  |")
            print("| 4 - revenir au menu principal |")
            print("+-------------------------------+")

            choice = input("Quel est votre choix : ")
            if not choice.isnumeric():
                print("Merci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)
        clear_screen()

        return choice