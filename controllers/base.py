import sys
from utils.utils_view import clear_screen
from models.database_model import DatabaseModel
from models.employee_model import EmployeeModel
from views.login_view import LoginMenu
from views.main_menu import MainMenu
from constants.base import MENU_CUSTOMERS, MENU_CONTRACTS, MENU_EVENTS, MENU_EMPLOYEES, MENU_EXIT
from constants.database import DB_URL
from controllers.customer_controller import CustomerController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController
from controllers.employee_controller import EmployeeController
from utils.utils_view import display_message
from utils.utils_database import create_departments, create_super_admin



class epicEvents:
    """ Epic Events class """

    def __init__(self):
        self.db = DatabaseModel(DB_URL)
        if not self.db.tables_exist():
            try:
                self.db.create_tables()
                create_departments(DB_URL)
                create_super_admin(DB_URL)
            except Exception as e:
                print(f"Une erreur s'est produite lors de l'initialisation de la base de données : {e}")
                sys.exit()
        self.login_view = LoginMenu()
        self.main_menu_view = MainMenu()
        self.customer_controller = CustomerController(self.db)
        self.contract_controller = ContractController(self.db)
        self.event_controller = EventController(self.db)
        self.employee_controller = EmployeeController()
        self.employee_model = EmployeeModel()

    def login_menu(self):
        """ login menu of Epic Events CRM """

        show_title = True
        authentication = False
        clear_screen()
        while authentication == False:
            input_username, input_password = self.login_view.login_menu(show_title)
            show_title = False
            employee_obj = self.employee_model.search_employee(input_username)
            if employee_obj:
                password_valid = self.employee_model.check_password(employee_obj.password, input_password)
                if password_valid:
                    authentication = True
                    self.main_menu(employee_obj.id)
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
            elif choice == MENU_CONTRACTS:
                self.contract_controller.menu_customer(employee_id)
            elif choice == MENU_EVENTS:
                self.event_controller.menu_event(employee_id)
            elif choice == MENU_EMPLOYEES:
                self.employee_controller.menu_employee(employee_id)
            elif choice == MENU_EXIT:
                self.login_menu()
