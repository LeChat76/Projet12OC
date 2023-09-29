import unittest
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.contract_model import ContractModel
from models.event_model import EventModel
from constants.department import COMMERCIAL
import bcrypt
from cryptography.fernet import Fernet


employee_id = 1

class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.employee = EmployeeModel()
        employee_obj = self.employee.search_employee(COMMERCIAL)
        self.employee.password = employee_obj.password

    def test_valid_password(self):
        # Test with valid password

        KEY = "aWbBVphsmr3o9E0DYyU6nIw07afqOIaMWRGUKHDbD4E="
        HASHED_PASSWORD = "gAAAAABlF0LnYTgI18lne029oXPElH6ugIHvQ0eElK-5wIelNvMftg8FAZ0cQfJcif1AVU369g976yNO7oc8sADpcGj3p3LC_A=="
        fernet = Fernet(KEY)
        input_password = fernet.decrypt(HASHED_PASSWORD).decode()

        self.assertTrue(
            self.employee.check_password(self.employee.password, input_password)
        )

    def test_invalid_password(self):
        # Test with invalid password
        input_password = "MauvaisPassword1234!"

        self.assertFalse(
            self.employee.check_password(self.employee.password, input_password)
        )

    def test_valid_username(self):
        # Test with existant username
        input_username = COMMERCIAL

        self.assertTrue(self.employee.search_employee(input_username))

    def test_invalid_username(self):
        # Test with inexistant username
        input_username = "intruder"

        self.assertFalse(self.employee.search_employee(input_username))

    def test_search_support_employee(self):
        # Test search of support department employee (in reality support AND superadmin department)

        self.assertTrue(self.employee.select_support_employee())

    def test_search_all_employees(self):
        # Test search all employees

        self.assertTrue(self.employee.select_all_employee())

    def test_create_employee_object_with_valid_employee_id(self):
        # test creation of an employee object with valid employee ID

        employee_id = 1

        self.assertTrue(self.employee.create_employee_object(employee_id))

    def test_create_employee_object_with_invalid_employee_id(self):
        # test creation of an employee object with valid employee ID

        employee_id = 666

        self.assertFalse(self.employee.create_employee_object(employee_id))

    def test_check_permission_with_valid_employee(self):
        # test if True when using a MANAGEMENT department employee

        employee_id = 3

        self.assertTrue(self.employee.check_permission_employee(employee_id))

    def test_check_permission_with_invalid_employee(self):
        # test if True when using an SUPPORT department employee

        employee_id = 2

        self.assertFalse(self.employee.check_permission_employee(employee_id))

    def test_create_employee_object_from_choice_list(self):
        # test of creation of employee object choice from a list

        choice = 1

        self.assertTrue(self.employee.create_employee_object_from_list(choice))

    def test_add_loggin_delete_employee_in_database(self):
        # Test adding employee in database

        salt = bcrypt.gensalt()

        employee_obj = EmployeeModel()
        employee_obj.username = ("TestUser",)
        employee_obj.password = "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i"
        employee_obj.email = ("cedrik76@msn.com",)
        employee_obj.department_id = 1
        self.assertTrue(self.employee.add_employee(employee_id, employee_obj))

        # Test of login with user TestUser
        self.assertTrue(self.employee.search_employee("TestUser"))
        # Test password of TestUser
        KEY = "aWbBVphsmr3o9E0DYyU6nIw07afqOIaMWRGUKHDbD4E="
        HASHED_PASSWORD = "gAAAAABlF0LnYTgI18lne029oXPElH6ugIHvQ0eElK-5wIelNvMftg8FAZ0cQfJcif1AVU369g976yNO7oc8sADpcGj3p3LC_A=="
        fernet = Fernet(KEY)
        password = fernet.decrypt(HASHED_PASSWORD).decode()
        self.assertTrue(
            self.employee.check_password(
                "$2b$12$e1/vhXWWcWCQZQKEi5DCruo3hPlLw4DVLdqXX0qMj7uDF49EZe6FK",
                password,
            )
        )

        # Test to delete employee in the database
        self.assertTrue(self.employee.delete_last_employee())


if __name__ == "__main__":
    unittest.main()
