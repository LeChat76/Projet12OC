from views.contract_view import ContractView
from views.customer_view import CustomerView
from models.contract_model import ContractModel
from models.customer_model import CustomerModel
from constants.contract import (
    MENU_CONTRACT_CREATION,
    MENU_CONTRACT_UPDATE,
    MENU_CONTRACT_SIGNATURE,
    MENU_CONTRACT_FILTER,
    MENU_CONTRACT_EXIT,
)
from constants.contract import (
    MENU_CONTRACT_FILTER_BY_SIGNATURE,
    MENU_CONTRACT_FILTER_NOT_FULLY_PAYED,
    MENU_CONTRACT_FILTER_EXIT,
)
from utils.utils_view import display_message, input_message


class ContractController:
    """Contract controller"""

    def __init__(self, db):
        self.db = db
        self.contract_view = ContractView()
        self.customer_view = CustomerView()
        self.customer_model = CustomerModel(None, None, None, None, None)
        self.contract_model = ContractModel(None, None, None, None, None)

    def menu_customer(self, employee_id):
        """Contract menu"""

        while True:
            choice = self.contract_view.contract_menu()
            if choice == MENU_CONTRACT_CREATION:
                self.add_contract(employee_id)
            elif choice == MENU_CONTRACT_UPDATE:
                self.update_contract(employee_id)
            elif choice == MENU_CONTRACT_SIGNATURE:
                self.sign_contract(employee_id)
            elif choice == MENU_CONTRACT_FILTER:
                permission = self.contract_model.check_permission_filter_menu(
                    employee_id
                )
                if permission:
                    while True:
                        filter_choice = self.contract_view.contract_menu_filter()
                        if filter_choice == MENU_CONTRACT_FILTER_BY_SIGNATURE:
                            self.filter_contract_by_signature()
                        elif filter_choice == MENU_CONTRACT_FILTER_NOT_FULLY_PAYED:
                            self.filter_contract_by_payed()
                        elif filter_choice == MENU_CONTRACT_FILTER_EXIT:
                            break
                elif not permission:
                    display_message(
                        "Vous n'êtes pas autorisé à accéder à ce menu...", True, True, 2
                    )
                    break
            elif choice == MENU_CONTRACT_EXIT:
                break

    def add_contract(self, employee_id):
        """creation of contract method"""

        # check permission of the logged employee to access to this menu
        permission = self.contract_model.check_permission(employee_id)
        if permission:
            new_contract_values = self.contract_view.add_contract()
            customer_name = self.customer_view.select_customer_by_entry()
            if not customer_name:
                customers_list = self.customer_model.search_all_customers()
                customer_choice = self.customer_view.select_customer_by_list(
                    customers_list
                )
                customer_obj = self.customer_model.create_customer_object(
                    customer_choice
                )
            else:
                customer_obj = self.customer_model.create_customer_object(customer_name)
            price = new_contract_values[0]
            due = new_contract_values[1]
            status = new_contract_values[2]
            new_contract_obj = ContractModel(
                price, due, status, customer_obj, employee_id
            )
            result = self.contract_model.add_contract(new_contract_obj)
            if result:
                display_message(
                    "Contrat créé avec succès. Retour au menu...",
                    True,
                    True,
                    2,
                )
            else:
                display_message(
                    "Erreur lors de l'ajout du contrat.\nVoir log Sentry.",
                    True,
                    True,
                    2,
                )
        else:
            display_message(
                "Vous n'êtes pas autorisé à créer des contrats. Retour au menu...",
                True,
                True,
                2,
            )

    def delete_contract(self, employee_id):
        """method to delete contract"""

        contracts_list = self.contract_model.search_all_contracts()
        if contracts_list:
            choice = ""
            # check permission to access to this menu
            permission = self.contract_model.check_permission(employee_id)
            if not permission:
                display_message(
                    "Vous n'avez pas la permission de supprimer des contrats. Retour au menu...",
                    True,
                    False,
                    2,
                )
            else:
                # display choice selection (bye input or list)
                contract_choice = self.contract_view.select_contract_by_entry()
                if not contract_choice:
                    contract_choice = self.contract_view.select_contract_by_list(
                        contracts_list
                    )
                if not contract_choice.lower() == "q":
                    # if valid choice : convert choice in object
                    contract_obj = self.contract_model.create_contract_object(
                        contract_choice
                    )
                    if contract_obj:
                        # check if contract is signed, if yes, deletion is forbidden
                        contract_signed_boolean = self.contract_model.check_signature(
                            contract_obj
                        )
                        if contract_signed_boolean:
                            display_message(
                                "Ce contrat est signé, interdit de le supprimer. Retour au menu...",
                                True,
                                False,
                                2,
                            )
                        else:
                            while choice.lower() != "o" and choice.lower() != "n":
                                choice = input_message(
                                    f"\nEtes vous sure de vouloir supprimer le contrat '{contract_obj.id} (o/N)? "
                                )
                                if choice.lower() == "o":
                                    result = self.contract_model.delete_contract(
                                        contract_obj.id
                                    )
                                    if result:
                                        display_message(
                                            f"Contrat numéro '{contract_obj.id}' supprimé avec succès!",
                                            True,
                                            True,
                                            2,
                                        )
                                    else:
                                        display_message(
                                            "Erreur lors de la suppresion du contrat.\nVoir logs Sentry.",
                                            True,
                                            True,
                                            2,
                                        )
                                elif choice.lower() == "n" or choice.lower() == "":
                                    display_message(
                                        "Annulation de la suppression. Retour au menu.",
                                        True,
                                        True,
                                        2,
                                    )
                                    break
                    else:
                        display_message(
                            "Aucun contrat trouvé avec ce nom. Retour au menu.",
                            True,
                            True,
                            2,
                        )
                else:
                    display_message("Retour au menu...", True, True, 2)
        else:
            display_message(
                "Aucun contrat dans la base de donnée. Retour au menu...", True, True, 2
            )

    def update_contract(self, employee_id):
        """update contract method"""

        contracts_list = self.contract_model.search_all_contracts()
        if contracts_list:
            # display choice selection (by input or list)
            contract_choice = self.contract_view.select_contract_by_entry()
            if contract_choice:
                check_if_contract_exists_boolean = (
                    self.contract_model.check_if_contract_exists(contract_choice)
                )
                if not check_if_contract_exists_boolean:
                    display_message(
                        "Ce numéro de contrat n'est pas repertorié dans la base de donnée.\nVeuillez choisir dans la liste des contrats non signés.",
                        False,
                        True,
                        2,
                    )
                    contracts_list = self.contract_model.search_all_contracts()
                    contract_choice = self.contract_view.select_contract_by_list(
                        contracts_list
                    )
            elif not contract_choice:
                contract_choice = self.contract_view.select_contract_by_list(
                    contracts_list
                )
            if not contract_choice.lower() == "q":
                # if valid choice : convert choice to object
                contract_obj = self.contract_model.create_contract_object(
                    contract_choice
                )
                if contract_obj:
                    # check permission to modify customer by the logged employee...
                    permission = self.contract_model.check_permission_on_contract(
                        employee_id, contract_obj
                    )
                    contract_signed_boolean = self.contract_model.check_signature(
                        contract_obj
                    )
                    if permission:
                        # .... if permit : display contract modification menu
                        contract_to_update_obj = self.contract_view.update_contract(
                            contract_obj
                        )
                        if contract_to_update_obj:
                            self.contract_model.update_contract(
                                contract_to_update_obj
                            )
                        else:
                            display_message(
                                "Aucune modification apportée au contrat, retour au menu.",
                                True,
                                True,
                                2,
                            )
                    else:
                        # ... if not permit : display contract info
                        self.contract_view.display_contract_informations(contract_obj)
            else:
                display_message("Retour au menu...", True, True, 2)
        else:
            display_message(
                "Aucun contrat dans la base de donnée. Retour au menu...", True, True, 2
            )

    def sign_contract(self, employee_id):
        """method to sign contract"""

        contract_obj = None

        not_signed_contracts_list = self.contract_model.select_not_signed_contract()
        if not_signed_contracts_list:
            choice = ""
            # check permission to access to this menu
            permission = self.contract_model.check_permission(employee_id)
            if not permission:
                display_message(
                    "Vous n'avez pas la permission de signer des contrats. Retour au menu...",
                    True,
                    False,
                    2,
                )
            else:
                # display choice selection (bye input or list)
                contract_choice = self.contract_view.select_contract_by_entry()
                if contract_choice:
                    check_if_contract_exists_boolean = (
                        self.contract_model.check_if_contract_exists(contract_choice)
                    )
                    if not check_if_contract_exists_boolean:
                        display_message(
                            "Ce numéro de contrat n'est pas repertorié dans la base de donnée.\nVeuillez choisir dans la liste des contrats non signés.",
                            True,
                            True,
                            2,
                        )
                        contract_choice = self.contract_view.select_contract_by_list(
                            not_signed_contracts_list
                        )
                    else:
                        contract_obj = self.contract_model.create_contract_object_with_id(contract_choice)
                elif not contract_choice:
                    not_signed_contracts_list = (
                        self.contract_model.select_not_signed_contract()
                    )
                    contract_choice = self.contract_view.select_contract_by_list(
                        not_signed_contracts_list
                    )
                if not contract_choice.lower() == "q":
                    # if valid choice : convert choice in object
                    if not contract_obj:
                        contract_choice = not_signed_contracts_list[int(contract_choice) - 1].id
                        contract_obj = self.contract_model.create_contract_object(
                            contract_choice
                    )
                    check_if_contract_signed_boolean = (
                        self.contract_model.check_signature(contract_obj)
                    )
                    if check_if_contract_signed_boolean:
                        display_message(
                            "Ce contrat est déjà signé. Retour au menu...",
                            True,
                            True,
                            2,
                        )
                    else:
                        while choice.lower() != "o" and choice.lower() != "n":
                            choice = input_message(
                                f"\nEtes vous sure de vouloir signer le contrat {contract_obj.id} (o/N)? "
                            )
                            if choice.lower() == "o":
                                self.contract_model.sign_contract(contract_obj)
                                display_message(
                                    f"Contrat numéro {contract_obj.id} signé. Retour au menu...",
                                    True,
                                    True,
                                    2,
                                )
                            elif choice.lower() == "n" or choice.lower() == "":
                                display_message(
                                    "Annulation de la signature. Retour au menu.",
                                    True,
                                    True,
                                    2,
                                )
                                break
                else:
                    display_message(
                        "Annulation de la signature. Retour au menu.", True, True, 2
                    )
        else:
            display_message(
                "Aucun contrat non signés dans la base de donnée. Retour au menu...",
                True,
                True,
                2,
            )

    def filter_contract_by_signature(self):
        """method to display contract without signature"""

        contracts_obj_list = self.contract_model.select_not_signed_contract()

        if contracts_obj_list:
            self.contract_view.display_contracts_by_list(contracts_obj_list)
        else:
            display_message(
                "Tous les contrats sont signés. Retour au menu...", True, True, 2
            )

    def filter_contract_by_payed(self):
        """method to display contract not fully payed"""

        contracts_obj_list = self.contract_model.select_not_fully_payed_contracts()

        if contracts_obj_list:
            self.contract_view.display_contracts_by_list(contracts_obj_list)
        else:
            display_message(
                "Tous les contrats sont payés. Retour au menu...", True, True, 2
            )
