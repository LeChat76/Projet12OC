def check_permission_menu(necessary_role, employee):
    """
    check authorization of the employee to access to a specific menu
    INPUT : type of menu (customer, contract or event) and employee object
    OUPUT : True or False
    """

    if necessary_role == employee.role or employee.role == 'superadmin':
        return True
    else:
        return False

def check_permission_customer(customer, employee):
    """
    function to check authorization of an employee on a customer
    (check if customer.employee_id == employee.id)
    INPUT : customer object + employee object
    OUTPUT : True of False
    """

    if customer.employee_id == employee.id or employee.role == 'superadmin':
        return True
    else:
        return False



