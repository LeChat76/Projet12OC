from views.utils_view import display_message
from views.event_view import EventView
from views.contract_view import ContractView
from views.employee_view import EmployeeView
from models.models import EventModel, ContractModel, EmployeeModel
from constants.event import MENU_EVENT_CREATION, MENU_EVENT_ASSIGNATION, MENU_EVENT_UPDATE, MENU_EVENT_DELETE, MENU_EVENT_EXIT


class EventController:
    """ Event controller class """

    def __init__(self, db):
        self.db = db
        self.event_view = EventView()
        self.contract_view = ContractView()
        self.employee_view = EmployeeView()
        self.event_model = EventModel()
        self.contract_model = ContractModel(None, None, None, None, None, None)
        self.employee_model = EmployeeModel()

    def menu_event(self, employee_id):
        """ Event menu """
    
        while True:
            choice = self.event_view.event_menu()
            if choice == MENU_EVENT_CREATION:
                self.add_event(employee_id)
            elif choice == MENU_EVENT_ASSIGNATION:
                self.assign_event(employee_id)
            elif choice == MENU_EVENT_UPDATE:
                self.update_event(employee_id)
            elif choice == MENU_EVENT_DELETE:
                pass
            elif choice == MENU_EVENT_EXIT:
                break

    def add_event(self, employee_id):
        """ creation of event method """

        # check permission of the logged employee to access to this menu
        permission = self.event_model.check_permission_event_creation(employee_id)
        if permission:
            contract_choice = self.contract_view.select_contract_by_entry()
            if contract_choice:
                check_if_contract_exists_boolean = self.contract_model.check_if_contract_exists(contract_choice)
                if not check_if_contract_exists_boolean:
                    display_message("Ce numéro de contrat n'est pas repertorié dans la base de donnée.\nVeuillez en choisir un dans la liste :", False, True, 2)
                    contracts_list = self.contract_model.search_all_contracts()
                    contract_choice = self.contract_view.select_contract_by_list(contracts_list)
            else:
                unassociated_contracts = self.contract_model.select_unassociated_contrats()
                contract_choice = self.contract_view.select_contract_by_list(unassociated_contracts)
            if not contract_choice.lower() == "q":
                contract_obj = self.contract_model.create_contract_object(contract_choice)
                new_event_tuple = self.event_view.add_event()
                new_event_obj = EventModel()
                new_event_obj.date_start = new_event_tuple[0]
                new_event_obj.date_end = new_event_tuple[1]
                new_event_obj.location = new_event_tuple[2]
                new_event_obj.attendees = new_event_tuple[3]
                new_event_obj.notes = new_event_tuple[4]
                new_event_obj.contract_id = contract_obj.id
                self.event_model.add_event(new_event_obj)
            else:
                display_message("Retour au menu...", True, True, 3)
        else:
            display_message("Vous n'avez pas les authorisations necessaire pour la creation d'évenements.\nRetour au menu...", True, True, 3)

    def assign_event(self, employee_id):
        """ method to assign an employee (from department support) to an event """

        employee_obj = None

        # check permission of the logged employee to access to this menu (if associated to support department)
        permission = self.event_model.check_permission_event_assignation(employee_id)
        if permission:
            while True:
                # create list of unassigned event
                not_assigned_event = self.event_model.select_unassigned_event()
                # create list of support and superadmin employees
                support_employees_obj_list = self.employee_model.select_support_employee()

                if not not_assigned_event:
                    display_message("Aucun evenement non assignés. Retour au menu...", True, True, 3)
                    break
                elif not support_employees_obj_list:
                    display_message("Aucun employee associé au service support dans la base de donnée.\nRetour au menu...", True, True, 3)
                    break
                else:
                    # selection of the event
                    event_choice = self.event_view.select_event_by_entry()
                    if event_choice:
                        check_if_event_exists = self.event_model.search_event(event_choice)
                        if not check_if_event_exists:
                            display_message("Ce numéro d'évenement n'existe pas. Selectionnez le par liste: ", False, True, 2)
                            event_choice = self.event_view.select_event_by_list(not_assigned_event)
                            if event_choice == "q":
                                display_message("Retour au menu...", False, True, 3)
                                break
                        else:
                            display_message("Evenement " + str(event_choice) + " trouvé.", False, True, 1)
                    else:
                        event_choice = self.event_view.select_event_by_list(not_assigned_event)
                        if event_choice == "q":
                            display_message("Retour au menu...", False, True, 3)
                            break

                    event_obj = not_assigned_event[(int(event_choice) - 1)]

                    # selection of the employee to assign to the selected event
                    employee_choice = self.employee_view.select_employee_by_entry()
                    if employee_choice:
                        employee_obj = self.employee_model.search_employee(employee_choice)
                        if employee_obj not in support_employees_obj_list:
                            display_message("Cet employé n'appartient pas au service support ou n'existe pas.\nSelectionnez un employee par liste: ", True, True, 2)
                            employee_choice = self.employee_view.select_employee_by_list(support_employees_obj_list)
                            if employee_choice == "q":
                                display_message("Retour au menu...", False, True, 3)
                                break
                    else:
                        employee_choice = self.employee_view.select_employee_by_list(support_employees_obj_list)
                        if employee_choice == "q":
                            display_message("Retour au menu...", False, True, 3)
                            break

                    if not employee_obj:
                        employee_obj = support_employees_obj_list[(int(employee_choice) - 1)]
                    
                    # assign de l'employee à l'evenement
                    self.event_model.assign_event(event_obj, employee_obj)

                    break

    def update_event(self, employee_id):
        """ method to update an event """
        pass