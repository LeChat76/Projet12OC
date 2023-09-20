import time


class EmployeeView:
    """ Employee view class"""

    def display_employee_list(self, employee_list):
        """
        display list of employee by department
        INPUT : employee obj list
        RESULT : display list of the provided employee
        """
    
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
            print()
            if choice.lower() == "q":
                return choice
            elif choice.isalpha():
                print("\nMerci de saisir un chiffre.\n")
            elif choice.isnumeric():
                if int(choice) >= counter_int:
                    print("\nCe choix ne fait pas parti de la liste...\n")
                else:
                    return choice

    
