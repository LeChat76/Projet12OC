from utils.utils import clear_screen
from constants.constants import MENU_CLIENTS, MENU_CONTRATS, MENU_EVENEMENTS, MENU_EXIT


class MainMenu:
    """ Main Menu Class """
    
    def main_menu(self):
        """ Root menu """
        choix = None
        while choix != MENU_CLIENTS and choix != MENU_CONTRATS\
                and choix != MENU_EVENEMENTS and choix != MENU_EXIT:
            clear_screen()
            print("+-------------------------------+")
            print("|             MENU              |")
            print("+-------------------------------+")
            print("| 1 - clients                   |")
            print("| 2 - contrats                  |")
            print("| 3 - evenements                |")
            print("| 4 - quitter                   |")
            print("+-------------------------------+")
            choix = input("Quel est votre choix : ")
            if not choix.isnumeric():
                print("Merci de préciser un choix numérique.")
                choix = None
            else:
                choix = int(choix)
        clear_screen()
        return choix
