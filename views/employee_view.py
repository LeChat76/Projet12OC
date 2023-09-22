import time, re
from getpass_asterisk.getpass_asterisk import getpass_asterisk
from constants.employee import MENU_EMPLOYEE_CREATION, MENU_EMPLOYEE_UPDATE, MENU_EMPLOYEE_DELETE, MENU_EMPLOYEE_EXIT
from views.utils_view import clear_screen


class EmployeeView:
    """ Employee view class"""


    def employee_menu(self):
        """ Menu 4 - EMPLOYEE """
        
        choice = None
        while choice !=  MENU_EMPLOYEE_CREATION and choice != MENU_EMPLOYEE_UPDATE and\
            choice != MENU_EMPLOYEE_DELETE and choice != MENU_EMPLOYEE_EXIT:
            clear_screen()
            print("+--------------------------------+")
            print("|          MENU JOUEUR           |")
            print("+--------------------------------+")
            print("| 1 - création d'un employe      |")
            print("| 2 - voir/modifier un employe   |")
            print("| 3 - suppression d'un employe   |")
            print("| 4 - revenir au menu principal  |")
            print("+--------------------------------+")

            choice = input("Quel est votre choix : ")
            if not choice.isnumeric():
                print("Merci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)

        return choice

    def add_employee(self, department_obj_list):
        """ method to add new employee """

        clear_screen()
        password_pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%:^&*])[a-zA-Z0-9!@#$%:^&*]{8,}$'
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        while True:
            username = input("Nom d'utilisateur (utilisé pour se connecter à l'application): ")
            if not username:
                print("\nNom d'utilisateur obligatoire. Merci d'en saisir un...\n")
            else:
                break

        while True:
            password = getpass_asterisk("\nMot de passe (8 caractères mini, au moins un chiffre, au moins un caractère spécial): ")
            if re.match(password_pattern, password):
                break
            else:
                print("\nLe mot de passe ne contient pas les critères requis. Ressaisir svp...")
        
        while True:
            email = input("\nEmail : ")
            if re.match(email_pattern, email):
                break
            else:
                print("\nLe format de l'email est incorrect. Ressaisir svp...")
        
        print("\nSelectionnez le department de l'utilisateur:\n")

        while True:
            choice_made = False
            counter_int = 1
            for department in department_obj_list:
                print(str(counter_int) + ' - ' + str(department))
                counter_int += 1
                time.sleep(0.1)
                if counter_int %5 == 0:
                    department_choice = input ("\nSaisir numero de ligne: ")
                    print()
                    if department_choice.isalpha():
                        print("\nMerci de saisir un chiffre.")
                    elif department_choice.isnumeric():
                        if int(department_choice) >= counter_int:
                            print("\nCe choix ne fait pas parti de la liste...\n")
                        else:
                            choice_made = True
                            break
            if choice_made:
                break

        description = input("Une description (non obligatoire)? ")

        return username, password, email, department_choice, description

    def select_employee_by_entry(self):
        """ selection of a employee by typing """

        while True:
            employee_name = input("\nQuel est le nom de l'employee [ENTRER pour afficher une liste]? ")
            print()
            return employee_name

    def select_employee_by_list(self, employees_list):
        """ selection of an employee by list """

        while True:
            counter_int = 1
            employee_id_list = []

            for employee in employees_list:
                print(str(counter_int) + ' - ' + str(employee))
                employee_id_list.append(employee.id)
                counter_int += 1
                time.sleep(0.1)
                if counter_int %5 == 0:
                    choice = input ("\nSaisir numero de ligne ([ENTRER] pour continuer ou (q)uitter)? ")
                    if choice.lower() == "q":
                        return choice
                    elif choice.isalpha():
                        print("\nMerci de saisir un chiffre.\n")
                    elif choice.isnumeric():
                        if int(choice) >= counter_int:
                            print("\nCe choix ne fait pas parti de la liste...\n")
                        else:
                            return choice
                    else:
                        print()

            choice = input("\nFin de liste atteinte. Faites un choix ou [ENTRER] pour relancer ou (q)uitter: ")
            if choice.lower() == "q":
                return choice
            elif choice.isalpha():
                print("\nMerci de saisir un chiffre.\n")
            elif choice.isnumeric():
                if int(choice) >= counter_int:
                    print("\nCe choix ne fait pas parti de la liste...\n")
                else:
                    return choice

    
