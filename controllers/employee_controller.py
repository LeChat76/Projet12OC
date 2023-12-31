from models.employee_model import EmployeeModel
from models.department_model import DepartmentModel
from views.employee_view import EmployeeView
from utils.utils_view import display_message, input_message
from constants.employee import (
    MENU_EMPLOYEE_CREATION,
    MENU_EMPLOYEE_UPDATE,
    MENU_EMPLOYEE_TOKEN,
    MENU_EMPLOYEE_DELETE,
    MENU_EMPLOYEE_EXIT,
)
from constants.token import SECRET_KEY
import bcrypt, jwt


class EmployeeController:
    """Employee controller class"""

    def __init__(self):
        self.employee_model = EmployeeModel()
        self.employee_view = EmployeeView()
        self.department_model = DepartmentModel()

    def menu_employee(self, employee_id):
        """Employee menu"""

        while True:
            choice = self.employee_view.employee_menu()
            if choice == MENU_EMPLOYEE_CREATION:
                self.add_employee(employee_id)
            elif choice == MENU_EMPLOYEE_UPDATE:
                self.update_employee(employee_id)
            elif choice == MENU_EMPLOYEE_DELETE:
                self.delete_employee(employee_id)
            elif choice == MENU_EMPLOYEE_TOKEN:
                self.generate_token(employee_id)
            elif choice == MENU_EMPLOYEE_EXIT:
                break

    def add_employee(self, employee_id):
        """method to add new employee"""

        salt = bcrypt.gensalt()

        # check permission to add employee
        permission = self.employee_model.check_permission_employee(employee_id)
        if not permission:
            display_message(
                "Vous n'avez pas les autorisations necessaires pour créer des utilisateurs.\nRetour au menu",
                True,
                True,
                2,
            )
        else:
            department_obj_list = self.department_model.select_all_department()
            new_employee_values_tuple = self.employee_view.add_employee(
                department_obj_list
            )
            department_obj = self.department_model.create_department_object_from_list(
                new_employee_values_tuple[3]
            )
            new_employee_obj = EmployeeModel()
            new_employee_obj.username = (new_employee_values_tuple[0],)
            new_employee_obj.password = (
                bcrypt.hashpw(new_employee_values_tuple[1].encode("utf-8"), salt),
            )
            new_employee_obj.email = (new_employee_values_tuple[2],)
            new_employee_obj.department_id = department_obj.id

            result = self.employee_model.add_employee(employee_id, new_employee_obj)
            if result:
                display_message("Employé ajouté avec succès!\nConsigné dans Sentry.", True, True, 2)
            else:
                display_message(
                    "Erreur lors de la creation de l'employé.\nVoir log Sentry pour plus d'informations.",
                    True,
                    True,
                    2,
                )

    def update_employee(self, employee_id):
        """method to update an employee"""

        # selection of the employee tu update
        while True:

            permission = self.employee_model.check_permission_employee(employee_id)
            if not permission:
                display_message(
                    "Vous n'etes pas autorisé à accéder à ce menu." +
                    "\nRetour au menu",
                    True,
                    True,
                    2)
                break
            else:
                all_employees = self.employee_model.select_all_employee()
                employee_choice = self.employee_view.select_employee_by_entry()

                if employee_choice:
                    employee_obj = self.employee_model.search_employee(employee_choice)
                    if not employee_obj:
                        display_message(
                            "Cet employé n'existe pas. Selectionnez le par liste: ",
                            False,
                            True,
                            2,
                        )
                        employee_choice = self.employee_view.select_employee_by_list(
                            all_employees
                        )
                        if employee_choice == "q":
                            display_message("Retour au menu...", True, True, 2)
                            break
                        else:
                            employee_obj = (
                                self.employee_model.create_employee_object_from_list(
                                    employee_choice
                                )
                            )
                else:
                    employee_choice = self.employee_view.select_employee_by_list(
                        all_employees
                    )
                    if employee_choice == "q":
                        display_message("Retour au menu...", True, True, 2)
                        break
                    else:
                        employee_obj = self.employee_model.create_employee_object_from_list(
                            employee_choice
                        )

                if not employee_choice == "q":

                    # check permission
                    permission = self.employee_model.check_permission_employee(employee_id)
                    if not permission:
                        self.employee_view.display_employee_informations(employee_obj)
                        break
                    else:
                        department_obj_list = self.department_model.select_all_department()
                        employee_to_update = self.employee_view.update_employee(
                            employee_obj, department_obj_list
                        )
                        if employee_to_update:
                            employee_obj = employee_to_update[0]
                            department_choice = employee_to_update[1]
                            if department_choice:
                                department_obj = self.department_model.create_department_object_from_list(
                                    department_choice
                                )
                                employee_obj.department_id = department_obj.id
                            result = self.employee_model.update_employee(employee_id, employee_obj)
                            if result:
                                display_message(
                                    f"Client '{employee_obj.username}' mis à jour avec succès!",
                                    True,
                                    True,
                                    2,
                                )
                            else:
                                display_message(
                                    "Erreur lors de la modification de l'employee. Voir logs Sentry",
                                    True,
                                    True,
                                    2,
                                )
                            break
                        else:
                            display_message(
                                "Aucune modification apportée à l'employee, retour au menu.",
                                True,
                                True,
                                2,
                            )
                            break

    def delete_employee(self, employee_id):
        """method to delete employees"""

        # check permission to access to this menu
        permission = self.employee_model.check_permission_employee(employee_id)
        if not permission:
            display_message(
                "Vous n'avez pas les autorisations necessaires pour supprimer des utilisateurs.\nRetour au menu",
                True,
                True,
                2,
            )
        else:
            while True:
                employees_obj_list = self.employee_model.select_all_employee()
                employee_choice = self.employee_view.select_employee_by_entry()
                if employee_choice:
                    employee_obj = self.employee_model.search_employee(employee_choice)
                    if not employee_obj:
                        display_message(
                            "Nom d'utilisateur introuvable. Merci de choisir par liste: ",
                            False,
                            True,
                            2,
                        )
                        employee_choice = self.employee_view.select_employee_by_list(
                            employees_obj_list
                        )
                        if employee_choice == "q":
                            display_message("Retour au menu...", True, True, 2)
                            break
                        else:
                            employee_obj = (
                                self.employee_model.create_employee_object_from_list(
                                    employee_choice
                                )
                            )
                else:
                    employee_choice = self.employee_view.select_employee_by_list(
                        employees_obj_list
                    )
                    if employee_choice == "q":
                        display_message("Retour au menu...", True, True, 2)
                        break
                    else:
                        employee_obj = (
                            self.employee_model.create_employee_object_from_list(
                                employee_choice
                            )
                        )

                choice = ""

                while choice.lower() != "o" and choice.lower() != "n":
                    choice = input_message(
                        f"\nEtes vous sure de vouloir supprimer l'employee '{employee_obj.username.capitalize()}' (o/N)? "
                    )
                    if choice.lower() == "o":
                        result = self.employee_model.delete_employee(employee_obj.id)
                        if result:
                            display_message(
                                f"Employé '{employee_obj.username}' supprimé avec succès!",
                                True,
                                True,
                                2,
                            )
                        else:
                            display_message(
                                "Erreur lors de la suppresion de l'employé.\nVoir log Sentry pour plus d'informations",
                                True,
                                True,
                                2,
                            )
                        break
                    elif choice.lower() == "n" or choice.lower() == "":
                        display_message(
                            "Annulation de la suppression. Retour au menu.",
                            True,
                            True,
                            2,
                        )
                        break
                break
    
    def generate_token(self, employee_id):
        """ method to generate token for auto login """

        # check permission to access to this menu
        permission = self.employee_model.check_permission_employee(employee_id)
        if not permission:
            display_message(
                "Vous n'avez pas les autorisations necessaires pour supprimer des utilisateurs" +
                ".\nRetour au menu.",
                True,
                True,
                2,
            )
        else:
            while True:
                employee_obj = None
                employee_choice = self.employee_view.select_employee_by_entry()
                if employee_choice:
                    employee_obj = self.employee_model.search_employee(employee_choice)
                    if not employee_obj:
                        display_message(
                            "Nom d'utilisateur introuvable. Merci de choisir par liste: ",
                            False,
                            True,
                            2,
                        )
                if not employee_obj:
                    employees_obj_list = self.employee_model.select_all_employee()
                    employee_choice = self.employee_view.select_employee_by_list(
                        employees_obj_list
                    )
                    if employee_choice == "q":
                        display_message("Retour au menu...", True, True, 2)
                        break
                    else:
                        employee_obj = (
                            self.employee_model.create_employee_object_from_list(
                                employee_choice
                            )
                        )
                user_data = {
                'user_id': employee_obj.id,
                'username': employee_obj.username,
                }
                token = jwt.encode(
                    {
                        'data': user_data
                    },
                    SECRET_KEY,
                    algorithm = 'HS256'
                )
                store_in_databse = self.employee_model.store_token_in_database(token, employee_obj.id)
                if not store_in_databse:
                    display_message("Erreur lors de l'enregistrement du token dans l'utilisateur.\n Voir log Sentry", True, True, 2)
                else:
                    store_in_file = self.employee_model.store_token_in_file(token)
                    if store_in_file:
                        display_message(
                            "Token stocké dans la base de donnée + fichier 'token.tkn'" + 
                            "\nExecutez la commande 'python.exe .\main.py --token' pour vous 'auto-connecter'." +
                            "\n([ENTRER] pour retourner au menu...)",
                            True,
                            True,
                            "pause"
                        )
                    else:
                        display_message(
                            "Erreur lors de l'enregistrement du token dans le fichier." +
                            "\nVoir logs Sentry.",
                            True,
                            True,
                            3
                        )
                break
