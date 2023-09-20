from views.utils_view import clear_screen
from constants.base import MENU_CUSTOMERS, MENU_CONTRACTS, MENU_EVENTS, MENU_EMPLOYEES, MENU_EXIT


class MainMenu:
    """ Main Menu Class """
    
    def main_menu(self):
        """ Root menu """

        choice = None
        while choice != MENU_CUSTOMERS and choice != MENU_CONTRACTS\
                and choice != MENU_EVENTS and choice != MENU_EXIT\
                and choice != MENU_EMPLOYEES:
            clear_screen()
            print("+--------------------------------+")
            print("|             MENU               |")
            print("+--------------------------------+")
            print("| 1 - clients                    |")
            print("| 2 - contrats                   |")
            print("| 3 - evenements                 |")
            print("| 4 - employees                  |")
            print("| 5 - quitter                    |")
            print("+--------------------------------+")
            choice = input("Quel est votre choix : ")
            if not choice.isnumeric():
                print("Merci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)
        clear_screen()
        return choice
