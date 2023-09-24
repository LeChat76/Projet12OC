from models.employee_model import EmployeeModel
from models.department_model import DepartmentModel
from views.employee_view import EmployeeView
from views.utils_view import display_message, input_message
from constants.employee import MENU_EMPLOYEE_CREATION, MENU_EMPLOYEE_UPDATE, MENU_EMPLOYEE_DELETE, MENU_EMPLOYEE_EXIT
import bcrypt


class EmployeeController:
    """ Employee controller class """

    def __init__(self):
        self.employee_model = EmployeeModel()
        self.employee_view = EmployeeView()
        self.department_model = DepartmentModel()

    def menu_employee(self, employee_id):
        """ Employee menu """
    
        while True:
            choice = self.employee_view.employee_menu()
            if choice == MENU_EMPLOYEE_CREATION:
                self.add_employee(employee_id)
            elif choice == MENU_EMPLOYEE_UPDATE:
                self.update_employee(employee_id)
            elif choice == MENU_EMPLOYEE_DELETE:
                self.delete_employee(employee_id)
            elif choice == MENU_EMPLOYEE_EXIT:
                break
    
    def add_employee(self, employee_id):
        """ method to add new employee """

        salt = bcrypt.gensalt()

        # check permission to add employee
        permission = self.employee_model.check_permission_employee(employee_id)
        if not permission:
            display_message("Vous n'avez pas les autorisations necessaires pour créer des utilisateurs.\nRetour au menu", True, True, 3)
        else:
            department_obj_list = self.department_model.select_all_department()
            new_employee_values_tuple = self.employee_view.add_employee(department_obj_list)
            department_obj = self.department_model.create_department_object_from_list(new_employee_values_tuple[3])
            new_employee_obj = EmployeeModel()
            new_employee_obj.username = new_employee_values_tuple[0],
            new_employee_obj.password = bcrypt.hashpw(new_employee_values_tuple[1].encode('utf-8'), salt),
            new_employee_obj.email = new_employee_values_tuple[2],
            new_employee_obj.department_id = department_obj.id,
            new_employee_obj.description = new_employee_values_tuple[4],

            self.employee_model.add_employee(new_employee_obj)
    
    def delete_employee(self, employee_id):
        """ method to delete employees """

        # check permission to access to this menu
        permission = self.employee_model.check_permission_employee(employee_id)
        if not permission:
            display_message("Vous n'avez pas les autorisations necessaires pour supprimer des utilisateurs.\nRetour au menu", True, True, 3)
        else:
            while True:
                employees_obj_list = self.employee_model.select_all_employee()
                employee_choice = self.employee_view.select_employee_by_entry()
                if employee_choice:
                    employee_obj = self.employee_model.search_employee(employee_choice)
                    if not employee_obj:
                        display_message("Nom d'utilisateur introuvable. Merci de choisir par liste: ", False, True, 2)
                        employee_choice = self.employee_view.select_employee_by_list(employees_obj_list)
                        if employee_choice == "q":
                            display_message("Retour au menu...", True, True, 3)
                            break
                        else:
                            employee_obj = self.employee_model.create_employee_object_from_list(employee_choice)
                else:
                    employee_choice = self.employee_view.select_employee_by_list(employees_obj_list)
                    if employee_choice == "q":
                        display_message("Retour au menu...", False, True, 3)
                        break
                    else:
                        employee_obj = self.employee_model.create_employee_object_from_list(employee_choice)

                choice = ""

                while choice.lower() != "o" and choice.lower() != "n":
                    choice = input_message(f"\nEtes vous sure de vouloir supprimer l'employee '{employee_obj.username.capitalize()}' (o/N)? ")
                    if choice.lower() == "o":
                        self.employee_model.delete_employee(employee_obj)
                        break
                    elif choice.lower() == "n" or choice.lower() == "":
                        display_message("Annulation de la suppression. Retour au menu.", True, True, 3)
                        break
                break
        