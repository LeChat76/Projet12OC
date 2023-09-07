import sys
from views.main_menu import MainMenu
from models.database import Database
from constants import MENU_CLIENTS, MENU_CONTRATS, MENU_EVENEMENTS, MENU_EXIT
from controllers.customer import CustomerController

class epicEvents:
    def __init__(self):
        self.view_main_menu = MainMenu()
        self.customer_controller = CustomerController()
        self.db = Database()
        self.db.create_tables()

    def main_menu(self):
        '''
        Display main menu of Epic Events CRM
        '''
        while True:
            choice = self.view_main_menu.main_menu()
            if choice == MENU_CLIENTS:
                self.customer_controller.menu_customer()
            elif choice == MENU_EXIT:
                sys.exit()
