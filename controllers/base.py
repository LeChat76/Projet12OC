import sys
from utils.utils import clear_screen
from models.models import Database
from models.employee_model import EmployeeModel
from views.login_view import LoginMenu
from views.main_menu import MainMenu
from constants.constants import MENU_CLIENTS, MENU_CONTRATS, MENU_EVENEMENTS, MENU_EXIT, DB_URL
from controllers.customer_controller import CustomerController


class epicEvents:
    def __init__(self):
        self.db = Database(DB_URL)
        self.login_view = LoginMenu()
        self.main_menu_view = MainMenu()
        self.customer_controller = CustomerController(self.db)
        self.employee_model = EmployeeModel()

    def login_menu(self):
        """ Display login menu of Epic Events CRM """

        show_title = True
        authentication = False
        clear_screen()
        while authentication == False:
            input_username, input_password = self.login_view.login_menu(show_title)
            show_title = False
            employee = self.employee_model.search_employee(input_username)
            if employee:
                password_valid = EmployeeModel.check_password(employee, input_password)
                if password_valid:
                    authentication = True
                    self.main_menu(employee)
                else:
                    print('\nPassword incorrect! Merci de resaisir.\n')
            else:
                print('\nUtilisateur inexistant.\n')

    def main_menu(self, employee):
        """ Display main menu """

        while True:
            choice = self.main_menu_view.main_menu()
            if choice == MENU_CLIENTS:
                self.customer_controller.menu_customer(employee)
            elif choice == MENU_EXIT:
                self.login_menu()

class BaseController:
    def __init__(self, db_url):
        self.db = Database(db_url)

    def initialize(self):
        """ db init """
        self.db.create_tables()
        self.db.create_superadmin()
