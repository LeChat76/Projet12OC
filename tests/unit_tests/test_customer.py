import unittest
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.contract_model import ContractModel
from models.event_model import EventModel


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.employee_id = 1
        self.customer_obj = CustomerModel(
            "Kevin Mitcnick",
            "kevin@mitnick.com",
            "0661994560",
            "KM Corp",
            self.employee_id,
        )
        self.customer_obj.id = 1000000

    def test_create_customer_in_database(self):
        # Test creation of customer in the database

        self.employee_id = "1"

        self.assertTrue(self.customer_obj.add_customer(self.customer_obj))

    def test_create_customer_object_with_name(self):
        # Test creation of customer with name

        self.assertTrue(
            self.customer_obj.create_customer_object_with_name(self.customer_obj.name)
        )

    def test_delete_customer_in_database(self):
        # Test deletion of customer in the database

        self.assertTrue(self.customer_obj.delete_last_customer())

    def test_check_permission_customer_menu(self):
        # Test permission to access to customer menu

        self.employee_id = 4  # employee of commercial employee (authorized employee)

        self.assertTrue(
            self.customer_obj.check_permission_customer_menu(self.employee_id)
        )

    def test_search_all_customers(self):
        # Test if selection of all customers works

        self.assertTrue(self.customer_obj.search_all_customers())

    def test_create_customer_object(self):
        # Test creation of customer object from choice in a list

        choice = "1"

        self.assertTrue(self.customer_obj.create_customer_object(choice))

    def test_create_customer_object_with_id(self):
        # Test creation of customer object with ID

        customer_id = 1

        self.assertTrue(self.customer_obj.create_customer_object_with_id(customer_id))

if __name__ == "__main__":
    unittest.main()