import time
from utils.utils_view import clear_screen
from views.customer_view import CustomerView
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


class ContractView:
    """Customer view class"""

    def __init__(self):
        self.customer_view = CustomerView()

    def contract_menu(self):
        """Menu 2 - CONTRAT"""

        choice = None
        while (
            choice != MENU_CONTRACT_CREATION
            and choice != MENU_CONTRACT_UPDATE
            and choice != MENU_CONTRACT_EXIT
            and choice != MENU_CONTRACT_SIGNATURE
            and choice != MENU_CONTRACT_FILTER
        ):
            clear_screen()
            print("+--------------------------------+")
            print("|          MENU CONTRAT         |")
            print("+--------------------------------+")
            print("| 1 - création d'un contrat      |")
            print("| 2 - voir/modifier un contrat   |")
            print("| 3 - signer un contrat          |")
            print("| 4 - filtrer contrats           |")
            print("|--------------------------------|")
            print("| 5 - revenir au menu principal  |")
            print("+--------------------------------+")

            choice = input("\nQuel est votre choix : ")
            if not choice.isnumeric():
                print("\nMerci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)

        return choice

    def contract_menu_filter(self):
        """Menu 2 - 5 contracts filter"""

        choice = None
        while (
            choice != MENU_CONTRACT_FILTER_BY_SIGNATURE
            and choice != MENU_CONTRACT_FILTER_NOT_FULLY_PAYED
            and choice != MENU_CONTRACT_FILTER_EXIT
        ):
            clear_screen()
            print("+--------------------------------+")
            print("|      MENU FILTRE CONTRAT       |")
            print("+--------------------------------+")
            print("| 1 - contrats non signés        |")
            print("| 2 - contrats non payés         |")
            print("|                                |")
            print("|                                |")
            print("|--------------------------------|")
            print("| 5 - revenir au menu principal  |")
            print("+--------------------------------+")

            choice = input("\nQuel est votre choix : ")
            if not choice.isnumeric():
                choice = None
            else:
                choice = int(choice)

        return choice

    def add_contract(self):
        """ask informations about new contract to add"""

        clear_screen()
        price, due = None, None

        while True:

            while True:
                price = input("Prix ([ENTRER] = 0€) : ")
                if price == "":
                    price = 0
                    break
                elif not price.isnumeric() and not price == "":
                    print("\nMerci de renseigner uniquement des chiffres.\n")
                else:
                    break

            while True:
                due = input(f"Montant restant du (< à {price}, [ENTRER = 0€] : ")
                if due == "":
                    due = 0
                    break
                elif not due.isnumeric() and not due == "":
                    print("\nMerci de renseigner uniquement des chiffres.\n")
                elif int(due) > int(price):
                    print(
                        "\nLe montant du ne peut pas etre superieur au montant du contrat.\n"
                    )
                else:
                    break

            while True:
                status = input("Contrat signé (o)ui/(n)on ([ENTRER] = non): ")
                if (
                    not status.lower() == "o"
                    and not status.lower() == "n"
                    and not status == ""
                ):
                    print("\nSaisie incorrect, reessayez svp.\n")
                elif status == "" or status.lower() == "n":
                    status = "NOT-SIGNED"
                    break
                else:
                    status = "SIGNED"
                    break

            return price, due, status

    def select_contract_by_entry(self):
        """selection of a contract by typing"""

        while True:
            contract_number = input(
                "\nQuel est le numero du contrat ([ENTRER] pour afficher une liste)? "
            )
            print()
            if not contract_number:
                return None
            elif not contract_number.isnumeric():
                print("\nMerci de saisir un chiffre.\n")
            else:
                print()
                return contract_number

    def select_contract_by_list(self, contracts_list):
        """selection of a contract by list"""

        # display list of contracts
        while True:
            counter_int = 1

            for contract in contracts_list:
                print(str(counter_int) + " - " + str(contract))
                counter_int += 1
                time.sleep(0.1)
                if counter_int % 5 == 0:
                    choice = input(
                        "\nQuel est votre choix ([ENTRER] pour continuer ou (q)uitter)? "
                    )
                    if choice.lower() == "q":
                        return choice
                    elif choice.isalpha():
                        print("Merci de saisir un chiffre/nombre\n")
                    elif choice.isnumeric():
                        if int(choice) >= counter_int:
                            print("\nCe choix ne fait pas parti de la liste...\n")
                        else:
                            return choice
                    else:
                        print()

            choice = input(
                "\nFin de liste atteinte. Faites un choix ou [ENTRER] pour relancer ou (q)uitter: "
            )
            print()
            if choice.lower() == "q":
                return choice
            elif choice.isalpha():
                print("Merci de saisir un chiffre/nombre\n")
            elif choice.isnumeric():
                if int(choice) >= counter_int:
                    print("\nCe choix ne fait pas parti de la liste...\n")
                else:
                    return choice

    def update_contract(self, contract_obj):
        """modifications input for a contract"""

        clear_screen()
        print("\nContrat selectionné :", contract_obj)
        print()

        # view and modify value for an contract

        modification_state_boolean = False

        while True:
            price = input(
                f"Prix actuel : '{contract_obj.price}' [ENTRER pour conserver prix actuel]: "
            )
            if price.isnumeric():
                modification_state_boolean = True
                contract_obj.price = price
                break
            elif not price:
                price = contract_obj.price
                break
            else:
                print("\nMerci de préciser un prix en chiffre...\n")

        while True:
            print(f"\nMontant restant du actuel : '{contract_obj.due}'")
            due = input(
                f"\nPreciser nouveau montant (< {contract_obj.price}) [ENTRER pour conserver montant actuel]: "
            )
            if due.isnumeric():
                if int(due) > int(price):
                    print(
                        "\nLe montant du ne peut pas etre superieur au montant du contrat.\n"
                    )
                else:
                    modification_state_boolean = True
                    contract_obj.due = due
                    break
            elif not due:
                break
            else:
                print("\nMerci de préciser un montant en chiffre...\n")

        # while True:
        #     if contract_obj.status == "NOT-SIGNED":
        #         status = input("\nSigner contrat? (o/N): ")
        #         if (
        #             not status.lower() == "o"
        #             and not status.lower() == "n"
        #             and not status == ""
        #         ):
        #             print("\nSaisie incorrect, reessayez svp.\n")
        #         elif status.lower() == "o":
        #             contract_obj.status = "SIGNED"
        #             modification_state_boolean = True
        #             break
        #         elif status.lower() == "n" or not status.lower():
        #             break
        #     else:
        #         print("\nCe contrat est déjà signé, on ne peut pas le 'déssigner' ;-)")
        #         time.sleep(2)
        #         break

        if modification_state_boolean:
            return contract_obj
        else:
            return None

    def sign_contract(self, contract_obj):
        """
        sign contract method
        INPUT : contract object
        OUTPUT : contract.status="SIGNED"
        """

        clear_screen()
        print("\nContrat selectionné :", contract_obj)
        while True:
            print()
            status = input("Contrat signé (o)ui/(n)on ([ENTRER] = non): ")
            if (
                not status.lower() == "o"
                and not status.lower() == "n"
                and not status == ""
            ):
                print("\nSaisie incorrect, reessayez svp.\n")
            elif status == "" or status.lower() == "n":
                print("\nRetour au menu...")
                time.sleep(3)
                break
            else:
                contract_obj.status = "SIGNED"
                self.contract_model.update_contract(contract_obj)
                print("\nContrat signé. Retour au menu...")
                time.sleep(3)
                break

    def display_contract_informations(self, contract_obj):
        """
        display contract information
        INPUT : contract object
        RESULT : display contract informations
        """

        print("\nVos droits ne vous donne accès qu'en lecture.\n")
        print(f"* Numéro           : {contract_obj.id}")
        print(f"* Prix             : {contract_obj.price}")
        print(f"* Due              : {contract_obj.due}")
        print(f"* Status           : {contract_obj.status}")
        input("\n[ENTRER] pour retourner au menu.\n")

    def display_contracts_by_list(self, contracts_obj_list):
        """
        method to display contracts by list
        INPUT : contracts objects list
        OUPUT : displaying contracts by list
        """

        choice = ""

        while True:
            counter_int = 1
            print()

            for contract in contracts_obj_list:
                print(" - " + str(contract))
                counter_int += 1
                time.sleep(0.1)
                if counter_int % 5 == 0:
                    choice = input(
                        "\nAppuyez sur [ENTRER] pour continuer ou (q)uitter)? "
                    )
                    if choice.lower() == "q":
                        break
                    else:
                        print()

            if choice.lower() == "q":
                print("\nRetour au menu...")
                time.sleep(3)
                break

            input(
                "\nFin de liste atteinte. Appuyez sur [ENTRER] pour retourner au menu..."
            )
            break
