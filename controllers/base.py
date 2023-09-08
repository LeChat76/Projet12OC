import sys, bcrypt
from views.utils_view import clear_screen
from models.models import Database, Employee
from views.login_view import LoginMenu
from views.main_menu import MainMenu
from constants import MENU_CLIENTS, MENU_CONTRATS, MENU_EVENEMENTS, MENU_EXIT
from controllers.customer_controller import CustomerController


class epicEvents:
    def __init__(self, db):
        self.db = db
        self.login_view = LoginMenu()
        self.main_menu_view = MainMenu()
        self.customer_controller = CustomerController(db)

    def login_menu(self):
        """ Display login menu of Epic Events CRM """
        show_title = True
        authentication = False
        clear_screen()
        while authentication == False:
            input_username, input_password = self.login_view.login_menu(show_title)
            show_title = False
            session = self.db.get_session()
            employee = session.query(Employee).filter_by(username=input_username).first()
            if employee:
                db_password = employee.password
                if bcrypt.checkpw(input_password.encode('utf-8'), db_password.encode('utf-8')):
                    authentication = True
                    self.main_menu(employee.id)
                else:
                    print('\nPassword incorrect! Merci de resaisir.\n')
            else:
                print('\nUtilisateur inexistant.\n')

    def main_menu(self, employee_id):
        """ Display main menu """

        while True:
            choice = self.main_menu_view.main_menu()
            if choice == MENU_CLIENTS:
                self.customer_controller.menu_customer(employee_id)
            elif choice == MENU_EXIT:
                sys.exit()

class BaseController:
    def __init__(self, db_url):
        self.db = Database(db_url)

    def initialize(self):
        """ db init """
        self.db.create_tables()
        self.db.create_superadmin()
