import time, re
from getpass_asterisk.getpass_asterisk import getpass_asterisk
from constants.employee import MENU_EMPLOYEE_CREATION, MENU_EMPLOYEE_UPDATE, MENU_EMPLOYEE_DELETE, MENU_EMPLOYEE_EXIT
from utils.utils_view import clear_screen
from getpass_asterisk.getpass_asterisk import getpass_asterisk
import bcrypt


class EmployeeView:
    """ Employee view class"""


    def employee_menu(self):
        """ Menu 4 - EMPLOYEE """
        
        choice = None
        while choice !=  MENU_EMPLOYEE_CREATION and choice != MENU_EMPLOYEE_UPDATE and\
            choice != MENU_EMPLOYEE_DELETE and choice != MENU_EMPLOYEE_EXIT:
            clear_screen()
            print("+--------------------------------+")
            print("|          MENU EMPLOYE          |")
            print("+--------------------------------+")
            print("| 1 - création d'un employe      |")
            print("| 2 - voir/modifier un employe   |")
            print("| 3 - suppression d'un employe   |")
            print("|                                |")
            print("|                                |")
            print("|--------------------------------|")
            print("| 6 - revenir au menu principal  |")
            print("+--------------------------------+")

            choice = input("\nQuel est votre choix : ")
            if not choice.isnumeric():
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

    def update_employee(self, employee_obj, department_obj_list):
        """ method to update an employee """

        clear_screen()
        print("\nEmployé selectionné :", employee_obj)
        print()

        password_pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%:^&*])[a-zA-Z0-9!@#$%:^&*]{8,}$'
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        salt = bcrypt.gensalt()

        modification_state_boolean = False
        department_chosen = False

        while True:
            employee_username = input(f"Nom de l'employee '{employee_obj.username}'. Changer ou [ENTRER] pour conserver actuel: ")
            if employee_username:
                modification_state_boolean = True
                employee_obj.username = employee_username
                break
            else:
                break
        
        while True:
            employee_password = getpass_asterisk("\nSaisir un nouveau mot de passe (ou [ENTRER] pour conserver actuel): ")
            if employee_password:
                if re.match(password_pattern, employee_password):
                    modification_state_boolean = True                    
                    employee_obj.password = bcrypt.hashpw(employee_password.encode('utf-8'), salt),
                    break
                else:
                    print("\nLe mot de passe ne contient pas les critères requis. Ressaisir svp...")
            else:
                break
        
        while True:
            employee_email = input(f"\nEmail de l'employé '{employee_obj.email}'. Saisir nouveau ou [ENTRER] pour conserver: ")
            if employee_email:
                if re.match(email_pattern, employee_email):
                    modification_state_boolean = True 
                    employee_obj.email = employee_email
                    break
                else:
                    print("\nLe format de l'email est incorrect. Ressaisir svp...")
            else:
                break
        
        while True:
            employee_department = input(f"\nDepartement de l'employé '{employee_obj.department}', changer? ('o' ou [ENTRER] pour conserver): ")
            if employee_department.lower()=="o":
                while True:
                    counter_int = 1
                    for department in department_obj_list:
                        print(str(counter_int) + ' - ' + str(department))
                        counter_int += 1
                        time.sleep(0.1)
                        if counter_int %5 == 0:
                            employee_department = input ("\nSaisir numero de ligne: ")
                            print()
                            if employee_department.isalpha():
                                print("\nMerci de saisir un chiffre.")
                            elif employee_department.isnumeric():
                                if int(employee_department) >= counter_int:
                                    print("\nCe choix ne fait pas parti de la liste...\n")
                                else:
                                    department_chosen = True
                    if department_chosen:
                        break
            break

        while True:
            if employee_obj.status == "ENABLE":
                employee_status = input("\nStatus actuel de l'employé 'ENABLE'. Passer à 'DISABLE'? (o/N)")
                if employee_status.lower() == "o":
                    modification_state_boolean = True
                    employee_obj.status = "DISABLE"
                    break
                elif employee_status.lower() == "n" or employee_status == "":
                    break
            elif employee_obj.status == "DISABLE":
                employee_status = input("\nStatus actuel de l'employé 'DISABLE'. Passer à 'ENABLE'? (o/N)")
                if employee_status.lower() == "o":
                    modification_state_boolean = True
                    employee_obj.status = "ENABLE"
                    break
            elif employee_status.lower() == "n" or employee_status == "":
                break
            else:
                break
        
        if modification_state_boolean:
            return employee_obj, employee_department
        else:
            return None

    def display_employee_informations(self, employee_obj):
        """
        display employee information
        INPUT : employee object
        RESULT : display employee informations
        """

        print("\nVos droits ne vous donne accès qu'en lecture.\n")
        print(f"* Username         : {employee_obj.username}")
        print(f"* Email            : {employee_obj.email}")
        print(f"* Departement      : {employee_obj.department.name}")
        print(f"* Status           : {employee_obj.status}")
        input("\n[ENTRER] pour retourner au menu.\n")

    
