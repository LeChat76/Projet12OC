import unittest
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.contract_model import ContractModel
from models.event_model import EventModel


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event = EventModel()

    def test_create_event_object_from_list(self):
        # Test creation of event object with choice from a list
        
        choice = 1

        self.assertTrue(self.event.create_event_object(choice))

    def test_permission_for_authorized_employee(self):
        # Test permission for authorized employee (COMMERCIAL or SUPERADMIN department)

        employee_id = 4

        self.assertTrue(self.event.check_permission_event(employee_id))
    
    def test_permission_for_unauthorized_employee(self):
        # Test permission for unauthorized employee (not COMMERCIAL or SUPERADMIN department)

        employee_id = 2

        self.assertFalse(self.event.check_permission_event(employee_id))

    def test_select_unassigned_event(self):
        # Test of selection of unassigned events

        self.assertTrue(self.event.select_unassigned_event())

    def test_search_event_by_number(self):
        # Test of selection of an event by ID

        event_id = 1

        self.assertTrue(self.event.search_event(event_id))

    def test_select_all_events(self):
        # Test of selection of all events

        self.assertTrue(self.event.select_all_events())

    def test_select_assigned_events(self):
        # Test of selection of all assigned events for an employee

        employee_id = 2

        self.assertTrue(self.event.select_assigned_events(employee_id))
    
    def test_add_update_event_in_database(self):
        # Test of adding event in the database

        event_obj = EventModel()
        event_obj.id = 1000000
        event_obj.date_start = "16/07/24 01:00"
        event_obj.date_end = "16/07/24 23:00"
        event_obj.location = "97 Allée des Platanes, 76520, Boos"
        event_obj.attendees = "10"
        event_obj.notes = ""
        event_obj.contract_id = "1"
        self.assertTrue(self.event.add_event(event_obj))

    def test_delete_event_in_database(self):
        # Test of deletion of an event in the database

        event_id = 1000000

        self.assertTrue(self.event.delete_event(event_id))

