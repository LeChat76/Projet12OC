import sys
from utils.utils_view import clear_screen
from models.database_model import DatabaseModel
from models.employee_model import EmployeeModel
from views.login_view import LoginMenu
from views.main_menu import MainMenu
from constants.database import DB_URL_ADMIN
from controllers.customer_controller import CustomerController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController
from controllers.employee_controller import EmployeeController
from utils.utils_view import display_message
from utils.utils_database import create_departments, create_super_admin, create_employees, create_contracts, create_events
from constants.base import (
    MENU_CUSTOMERS,
    MENU_CONTRACTS,
    MENU_EVENTS,
    MENU_EMPLOYEES,
    MENU_EXIT,
    CREATE_SAMPLES,
)


class epicEvents:
    """Epic Events class"""

    def __init__(self):
        self.db = DatabaseModel(DB_URL_ADMIN)
        if not self.db.tables_exist():
            try:
                self.db.create_tables()
                create_departments()
                create_super_admin()
            except Exception as e:
                print(
                    f"Une erreur s'est produite lors de l'initialisation de la base de données : {e}"
                )
                sys.exit()
        self.login_view = LoginMenu()
        self.main_menu_view = MainMenu()
        self.customer_controller = CustomerController(self.db)
        self.contract_controller = ContractController(self.db)
        self.event_controller = EventController(self.db)
        self.employee_controller = EmployeeController()
        self.employee_model = EmployeeModel()

    def login_menu(self, autologin):
        """login menu of Epic Events CRM"""
        
        while True:
            if autologin:
                token = self.employee_model.read_token()
                if token:
                    employee_obj = self.employee_model.create_employee_obj_ty_token(token)
                    if employee_obj:
                        self.main_menu(employee_obj.id)
                        break
                    else:
                        display_message(
                            "Ce token ne correspond à aucun utilisateur." +
                            "\nMerci de renseigner vos identifiants.",
                            True,
                            True,
                            2)
                else:
                    display_message("Aucun fichier 'token.tkn' trouvé." +
                                    "\nMerci de renseigner vos identifiants.",
                                    True,
                                    True,
                                    2
                                    )
                    
            show_title = True
            authentication = False
            clear_screen()
            
            while authentication == False:
                input_username, input_password = self.login_view.login_menu(show_title)
                show_title = False
                employee_obj = self.employee_model.search_employee(input_username)
                if employee_obj:
                    password_valid = self.employee_model.check_password(
                        employee_obj.password, input_password
                    )
                    if password_valid:
                        authentication = True
                        self.main_menu(employee_obj.id)
                        break
                    else:
                        display_message(
                            "Password incorrect! Merci de resaisir.", True, True, 0
                        )
                else:
                    display_message("Utilisateur inexistant.", True, True, 0)

    def main_menu(self, employee_id):
        """main menu"""

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
            elif choice == CREATE_SAMPLES:
                create_employees()
                create_contracts()
                create_events()
            elif choice == MENU_EXIT:
                self.login_menu(None)
