from utils.utils_view import clear_screen
from constants.base import (
    MENU_CUSTOMERS,
    MENU_CONTRACTS,
    MENU_EVENTS,
    MENU_EMPLOYEES,
    MENU_EXIT,
)


class MainMenu:
    """Main Menu Class"""

    def main_menu(self):
        """Root menu"""

        choice = None
        while (
            choice != MENU_CUSTOMERS
            and choice != MENU_CONTRACTS
            and choice != MENU_EVENTS
            and choice != MENU_EXIT
            and choice != MENU_EMPLOYEES
        ):
            clear_screen()
            print("+--------------------------------+")
            print("|        MENU PRINCIPAL          |")
            print("+--------------------------------+")
            print("| 1 - clients                    |")
            print("| 2 - contrats                   |")
            print("| 3 - evenements                 |")
            print("| 4 - employees                  |")
            print("|                                |")
            print("|--------------------------------|")
            print("| 6 - quitter                    |")
            print("+--------------------------------+")
            choice = input("\nQuel est votre choix : ")
            if not choice.isnumeric():
                choice = None
            else:
                choice = int(choice)
        clear_screen()
        return choice
