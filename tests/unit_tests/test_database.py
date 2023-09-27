import unittest
from models.database_model import DatabaseModel
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.contract_model import ContractModel
from models.event_model import EventModel
from constants.database import DB_URL


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = DatabaseModel(DB_URL)

    def test_tables_exist(self):
        # Test check if tables exist

        self.assertTrue(self.database.tables_exist())

if __name__ == "__main__":
    unittest.main()