import sys
from views.utils_view import clear_screen
from models.models import Database
from models.models import EmployeeModel
from views.login_view import LoginMenu
from views.main_menu import MainMenu
from constants.base import MENU_CUSTOMERS, MENU_CONTRACTS, MENU_EVENTS, MENU_EXIT
from constants.database import DB_URL
from controllers.customer_controller import CustomerController
from controllers.contract_controller import ContractController
from views.utils_view import display_message


class epicEvents:
    """ Epic Events class """

    def __init__(self):
        self.db = Database(DB_URL)
        if not self.db.tables_exist():
            try:
                self.db.create_tables()
            except Exception as e:
                print(f"Une erreur s'est produite lors de l'initialisation de la base de données : {e}")
                sys.exit()
        self.login_view = LoginMenu()
        self.main_menu_view = MainMenu()
        self.customer_controller = CustomerController(self.db)
        self.contract_controller = ContractController(self.db)
        self.employee_model = EmployeeModel()

    def login_menu(self):
        """ login menu of Epic Events CRM """

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
                    self.main_menu(employee.id)
                else:
                    display_message("Password incorrect! Merci de resaisir.", True, True, 0)
            else:
                display_message("Utilisateur inexistant.", True, True, 0)

    def main_menu(self, employee_id):
        """ main menu """

        while True:
            choice = self.main_menu_view.main_menu()
            if choice == MENU_CUSTOMERS:
                self.customer_controller.menu_customer(employee_id)
            if choice == MENU_CONTRACTS:
                self.contract_controller.menu_customer(employee_id)
            if choice == MENU_EVENTS:
                pass
            elif choice == MENU_EXIT:
                self.login_menu()
