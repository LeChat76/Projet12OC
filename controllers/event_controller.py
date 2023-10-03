from utils.utils_view import display_message, input_message
from views.event_view import EventView
from views.contract_view import ContractView
from views.employee_view import EmployeeView
from models.event_model import EventModel
from models.contract_model import ContractModel
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from constants.event import (
    MENU_EVENT_CREATION,
    MENU_EVENT_ASSIGNATION,
    MENU_EVENT_UPDATE,
    MENU_EVENT_FILTER,
    MENU_EVENT_EXIT,
)
from constants.event import (
    MENU_EVENT_FILTER_NOT_ASSIGNED,
    MENU_EVENT_FILTER_IN_PROGRESS,
    MENU_EVENT_FILTER_ASSIGNED,
    MENU_EVENT_FILTER_EXIT,
)


class EventController:
    """Event controller class"""

    def __init__(self, db):
        self.db = db
        self.event_view = EventView()
        self.contract_view = ContractView()
        self.employee_view = EmployeeView()
        self.event_model = EventModel()
        self.contract_model = ContractModel(None, None, None, None, None)
        self.customer_model = CustomerModel(None, None, None, None, None)
        self.employee_model = EmployeeModel()

    def menu_event(self, employee_id):
        """Event menu"""

        while True:
            choice = self.event_view.event_menu()
            if choice == MENU_EVENT_CREATION:
                self.add_event(employee_id)
            elif choice == MENU_EVENT_ASSIGNATION:
                self.assign_event(employee_id)
            elif choice == MENU_EVENT_UPDATE:
                self.update_event(employee_id)
            elif choice == MENU_EVENT_FILTER:
                permission_management = (
                    self.event_model.check_permission_event_assignation(employee_id)
                )
                permission_support = (
                    self.event_model.check_permission_menu_filter_event(employee_id)
                )
                while True:
                    filter_choice = self.event_view.event_menu_filter()
                    if filter_choice == MENU_EVENT_FILTER_NOT_ASSIGNED:
                        if permission_management:
                            self.filter_event_not_assigned()
                        else:
                            display_message(
                                "Vous n'êtes pas autorisé à accéder à ce menu...",
                                True,
                                True,
                                2,
                            )
                    elif filter_choice == MENU_EVENT_FILTER_IN_PROGRESS:
                        if permission_management:
                            self.filter_event_in_progress()
                        else:
                            display_message(
                                "Vous n'êtes pas autorisé à accéder à ce menu...",
                                True,
                                True,
                                2,
                            )
                    elif filter_choice == MENU_EVENT_FILTER_ASSIGNED:
                        if permission_support:
                            self.filter_event_assigned(employee_id)
                        else:
                            display_message(
                                "Vous n'êtes pas autorisé à accéder à ce menu...",
                                True,
                                True,
                                2,
                            )
                    elif filter_choice == MENU_EVENT_FILTER_EXIT:
                        break

            elif choice == MENU_EVENT_EXIT:
                break

    def add_event(self, employee_id):
        """creation of event method"""

        contract_choice = None
        contract_obj = None

        # check permission of the logged employee to access to this menu
        permission = self.event_model.check_permission_event(employee_id)
        if permission:
            # check if available contracts (not associated to an event + not signed)
            available_contracts = self.contract_model.select_available_contracts(employee_id)
            if not available_contracts:
                display_message(
                    "Aucun contrat disponibles. Retour au menu...", True, True, 2
                )
            else:
                while True:
                    contract_choice = self.contract_view.select_contract_by_entry()
                    if contract_choice:
                        contract_obj = (
                            self.contract_model.create_contract_object_with_id(
                            contract_choice
                            )
                        )
                        if not contract_obj or not contract_obj in available_contracts:
                            display_message(
                                "Ce numéro de contrat n'est pas repertorié dans la base de donnée" +
                                "\nou n'est pas associé à un de vos clients.\nVeuillez en choisir un dans la liste :",
                                False,
                                True,
                                1,
                            )
                            contract_choice = (
                                self.contract_view.select_contract_by_list(
                                    available_contracts
                                )
                            )
                        else:
                            contract_obj = self.contract_model.create_contract_object_with_id(contract_choice)
                    else:
                        contract_choice = self.contract_view.select_contract_by_list(
                            available_contracts
                        )
                        # contract_id = available_contracts[int(contract_choice) - 1].id
                    if not contract_choice.lower() == "q":
                        if not contract_obj:
                            contract_obj = self.contract_model.create_contract_object_with_id(
                                available_contracts[int(contract_choice) - 1].id
                            )
                        permission = self.contract_model.check_if_contract_associated_to_employee(
                            employee_id, contract_obj
                        )
                        if permission:
                            new_event_tuple = self.event_view.add_event()
                            new_event_obj = EventModel()
                            new_event_obj.date_start = new_event_tuple[0]
                            new_event_obj.date_end = new_event_tuple[1]
                            new_event_obj.location = new_event_tuple[2]
                            new_event_obj.attendees = new_event_tuple[3]
                            new_event_obj.notes = new_event_tuple[4]
                            new_event_obj.contract_id = contract_obj.id
                            result = self.event_model.add_event(new_event_obj)
                            if result:
                                display_message(
                                    "Evenement ajouté avec succès !", True, True, 2
                                )
                            else:
                                display_message(
                                    f"Erreur lors de l'ajout de l'evenement.\nVoir logs Sentry pour plus d'informations.",
                                    True,
                                    True,
                                    2,
                                )
                            break
                        else:
                            display_message(
                                "Le client associé à ce contrat ne vous appartient pas. Recommencez...",
                                True,
                                True,
                                2,
                            )
                    else:
                        display_message("Retour au menu...", True, True, 2)
                        break
        else:
            display_message(
                "Vous n'avez pas les authorisations necessaire pour la creation d'évenements.\nRetour au menu...",
                True,
                True,
                2,
            )

    def assign_event(self, employee_id):
        """method to assign an employee (from department support) to an event"""

        employee_obj = None

        # check permission of the logged employee to access to this menu (if associated to support department)
        permission = self.event_model.check_permission_event_assignation(employee_id)
        if not permission:
            display_message(
                "Vous n'avez les autorisations necessaire pour assigner un evenement à un employé.\nRetour au menu...",
                True,
                True,
                2,
            )
        else:
            while True:
                # create list of unassigned event
                not_assigned_event = self.event_model.select_unassigned_event()
                # create list of support and superadmin employees
                support_employees_obj_list = (
                    self.employee_model.select_support_employee()
                )

                if not not_assigned_event:
                    display_message(
                        "Aucun evenement non assignés. Retour au menu...", True, True, 2
                    )
                    break
                elif not support_employees_obj_list:
                    display_message(
                        "Aucun employee associé au service support dans la base de donnée.\nRetour au menu...",
                        True,
                        True,
                        2,
                    )
                    break
                else:
                    # selection of the event
                    event_choice = self.event_view.select_event_by_entry()
                    if event_choice:
                        event_obj = self.event_model.search_event(
                            event_choice
                        )
                        if not event_obj or all(obj.id != event_obj.id for obj in not_assigned_event):
                            display_message(
                                "Ce numéro d'évenement n'existe pas ou est déjà assigné. Selectionnez le par liste: ",
                                False,
                                True,
                                2,
                            )
                            event_choice = self.event_view.select_event_by_list(
                                not_assigned_event
                            )
                            if event_choice == "q":
                                display_message("Retour au menu...", True, True, 2)
                                break
                            else:
                                event_obj = not_assigned_event[(int(event_choice) - 1)]
                        else:
                            display_message(
                                "Evenement " + str(event_choice) + " trouvé.",
                                False,
                                False,
                                1,
                            )
                    else:
                        event_choice = self.event_view.select_event_by_list(
                            not_assigned_event
                        )
                        if event_choice == "q":
                            display_message("Retour au menu...", True, True, 2)
                            break
                        else:
                            event_obj = not_assigned_event[(int(event_choice) - 1)]

                    # selection of the employee to assign to the selected event
                    employee_choice = self.employee_view.select_employee_by_entry()
                    if employee_choice:
                        employee_obj = self.employee_model.search_employee(
                            employee_choice
                        )
                        if employee_obj not in support_employees_obj_list:
                            display_message(
                                "Cet employé n'appartient pas au service support ou n'existe pas.\nSelectionnez un employee par liste: ",
                                True,
                                True,
                                2,
                            )
                            employee_obj = None
                            employee_choice = (
                                self.employee_view.select_employee_by_list(
                                    support_employees_obj_list
                                )
                            )
                            if employee_choice == "q":
                                display_message("Retour au menu...", True, True, 2)
                                break
                    else:
                        employee_choice = self.employee_view.select_employee_by_list(
                            support_employees_obj_list
                        )
                        if employee_choice == "q":
                            display_message("Retour au menu...", True, True, 2)
                            break

                    if not employee_obj:
                        employee_obj = support_employees_obj_list[
                            (int(employee_choice) - 1)
                        ]

                    # assign de l'employee à l'evenement
                    self.event_model.assign_event(event_obj, employee_obj)

                    break

    def update_event(self, employee_id):
        """method to update an event"""

        # selection of the event tu update
        while True:

            all_events = self.event_model.select_all_events()
            if not all_events:
                display_message("Aucun evenement, retour au menu...", True, True, 2)
                break

            event_choice = self.event_view.select_event_by_entry()

            if event_choice:
                event_obj = self.event_model.search_event(event_choice)
                if not event_obj:
                    display_message(
                        "Ce numéro d'évenement n'existe pas. Selectionnez le par liste: ",
                        False,
                        True,
                        2,
                    )
                    event_choice = self.event_view.select_event_by_list(all_events)
                    if event_choice == "q":
                        display_message("Retour au menu...", True, True, 2)
                        break
                    else:
                        event_obj = self.event_model.create_event_object(event_choice)
            else:
                event_choice = self.event_view.select_event_by_list(all_events)
                if event_choice == "q":
                    display_message("Retour au menu...", True, True, 2)
                    break
                else:
                    event_obj = self.event_model.create_event_object(event_choice)

            if not event_choice == "q":
                contract_obj = self.contract_model.create_contract_object_with_id(
                    event_obj.contract_id
                )
                customer_obj = self.customer_model.create_customer_object_with_id(
                    contract_obj.customer_id
                )
                employee_obj = self.employee_model.create_employee_object(
                    event_obj.employee_id
                )

                # check permission
                permission = self.event_model.check_permission_event_update(
                    employee_id, event_obj
                )
                if not permission:
                    self.event_view.display_event_informations(
                        event_obj, customer_obj, employee_obj
                    )
                    break
                else:
                    event_to_update = self.event_view.update_event(event_obj)
                    if event_to_update:
                        result = self.event_model.update_event(event_to_update)
                        if result:
                            display_message(
                                f"Evenement '{event_to_update.id}' mis à jour avec succès!",
                                True,
                                True,
                                2,
                            )
                        else:
                            display_message(
                                "Erreur lors de la mise à jour de l'evenement.\nVoir logs Sentry.",
                                True,
                                True,
                                2,
                            )
                        break
                    else:
                        display_message(
                            "Aucune modification apportée à l'evenement, retour au menu.",
                            True,
                            True,
                            2,
                        )
                        break

    def delete_event(self, employee_id):
        """method to delete an event"""

        choice = ""

        # check permission to access to this menu
        permission = self.event_model.check_permission_event(employee_id)
        if not permission:
            display_message(
                "Vous n'avez pas les autorisations necessaires pour supprimer un evenement.\nRetour au menu...",
                True,
                True,
                2,
            )
        else:
            # check if events in database
            all_events = self.event_model.select_all_events()
            if not all_events:
                display_message("Aucun evenement, retour au menu...", True, True, 2)
            else:
                while True:
                    # selection of the event to delete
                    event_choice = self.event_view.select_event_by_entry()
                    if event_choice:
                        event_obj = self.event_model.search_event(event_choice)
                        if not event_obj:
                            display_message(
                                "Ce numéro d'évenement n'existe pas. Selectionnez le par liste: ",
                                False,
                                True,
                                2,
                            )
                            event_choice = self.event_view.select_event_by_list(
                                all_events
                            )
                            if event_choice == "q":
                                display_message("Retour au menu...", True, True, 2)
                                break
                            else:
                                event_obj = self.event_model.create_event_object(
                                    event_choice
                                )
                                break
                        else:
                            break
                    else:
                        event_choice = self.event_view.select_event_by_list(all_events)
                        if event_choice == "q":
                            display_message("Retour au menu...", True, True, 2)
                            break
                        else:
                            event_obj = self.event_model.create_event_object(
                                event_choice
                            )
                            break

                if not event_choice == "q":
                    while choice.lower() != "o" and choice.lower() != "n":
                        choice = input_message(
                            f"\nEtes vous sure de vouloir supprimer l'evenement numéro '{event_obj.id} (o/N)? "
                        )
                        if choice.lower() == "o":
                            result = self.event_model.delete_event(event_obj.id)
                            if result:
                                display_message(
                                    f"Evenement numero '{event_obj.id}' supprimé avec succès!",
                                    True,
                                    True,
                                    2,
                                )
                            else:
                                display_message(
                                    f"Erreur lors de la suppresion de l'evenement.\n(voir logs Sentry pour plus de détails).",
                                    True,
                                    True,
                                    2,
                                )
                            break
                        elif choice.lower() == "n" or choice.lower() == "":
                            display_message(
                                "Annulation de la suppression. Retour au menu.",
                                True,
                                True,
                                2,
                            )
                            break

    def filter_event_not_assigned(self):
        """method to display events not assigned to support employee"""

        events_obj_list = self.event_model.select_unassigned_event()

        if events_obj_list:
            self.event_view.display_events_by_list(events_obj_list)
        else:
            display_message(
                "Tous les évènements sont assignés. Retour au menu...", True, True, 2
            )

    def filter_event_in_progress(self):
        """method to display event not yet finished"""

        events_obj_list = self.event_model.select_in_progress_event()

        if events_obj_list:
            self.event_view.display_events_by_list(events_obj_list)
        else:
            display_message(
                "Aucun évènement en cours. Retour au menu...", True, True, 2
            )

    def filter_event_assigned(self, employee_id):
        """method to display assigned events"""

        events_obj_list = self.event_model.select_assigned_events(employee_id)

        if events_obj_list:
            self.event_view.display_events_by_list(events_obj_list)
        else:
            display_message(
                "Vous n'avez aucun évènement assigné. Retour au menu...", True, True, 2
            )
