import os


def clear_screen():
    """ function to clear screen """

    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system('cls')

def check_permission(menu, employee):
    """ function to check authorization of the employee """
    print('ROLE', employee.role)
    input()
    if menu == employee.role or employee.role == 'superadmin':
        return True
    else:
        return False

def check_if_customer_exists(customer):
    pass
