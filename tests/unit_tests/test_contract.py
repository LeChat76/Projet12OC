import unittest
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.contract_model import ContractModel
from models.event_model import EventModel


class TestContract(unittest.TestCase):
    def setUp(self):
        employee_id = 4
        self.customer_obj = CustomerModel(
            "Kevin Mitcnick", "kevin@mitnick.com", "0661994560", "KM Corp", employee_id
        )
        self.customer_obj.id = 1000000
        self.contract_obj = ContractModel(
            "Contrat de test", "1500", "500", "SIGNED", self.customer_obj, 4
        )
        self.contract_obj.id = 1000000

    def test_create_contract_in_database(self):
        # Test creation of contract in the database

        self.assertTrue(self.contract_obj.add_contract(self.contract_obj))

    # def test_check_if_contract_exists(self):
    #     # Test if contract 1000000 exists

    #     self.assertTrue(self.contract_obj.check_if_contract_exists("1000000"))

    def test_delete_contract_in_database(self):
        # Test deletion of contract in database

        self.assertTrue(self.contract_obj.delete_contract("1000000"))

    def test_create_contract_object(self):
        # Test creation of contract object chosen from list

        choice = 1

        self.assertTrue(self.contract_obj.create_contract_object(choice))

    def test_check_permission(self):
        # Test permission to access to contract menu

        employee_id = 3  # commercial employee (authorized employee)

        self.assertTrue(self.contract_obj.check_permission(employee_id))

        employee_id = 2  # support employee (unauthorizer employee)

        self.assertFalse(self.contract_obj.check_permission(employee_id))

    def test_check_permission_filter_menu(self):
        # Test access to filter contract menu

        employee_id = 1  # commercial employee (authorized employee)

        self.assertTrue(self.contract_obj.check_permission_filter_menu(employee_id))

    def test_select_not_fully_payed_contracts(self):
        # Test not fully payed contracts

        self.assertTrue(self.contract_obj.select_not_fully_payed_contracts())

    def test_select_not_signed_contract(self):
        # Test select not signed contract

        self.assertTrue(self.contract_obj.select_not_signed_contract())

    def test_search_all_contracts(self):
        # Test serach all contract

        self.assertTrue(self.contract_obj.search_all_contracts())

    def test_select_available_contracts(self):
        # Test select available contracts

        self.assertTrue(self.contract_obj.select_available_contracts())

    def tearDown(self):
        # delete test customer ID 1000000 after all test
        self.customer_obj.delete_customer("1000000")
