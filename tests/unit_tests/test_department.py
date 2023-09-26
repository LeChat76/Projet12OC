import unittest
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.contract_model import ContractModel
from models.event_model import EventModel


class TestDepartment(unittest.TestCase):
    def setUp(self):
        self.department = DepartmentModel()

    def test_create_department_object_from_list(self):
        # Test creation of department object with choice from a list
        
        choice = 1

        self.assertTrue(self.department.create_department_object_from_list(choice))

    def test_select_all_department(self):
        # Test selection of all department

        self.assertTrue(self.department.select_all_department())

