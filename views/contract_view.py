import time
from views.utils_view import clear_screen
from views.customer_view import CustomerView
from constants.contract import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_DELETE, MENU_CONTRACT_SIGNATURE, MENU_CONTRACT_EXIT


class ContractView:
    """ Customer view class """

    def __init__(self):
        self.customer_view = CustomerView()

    def contract_menu(self):
        """ Menu 2 - CONTRAT """

        choice = None
        while choice !=  MENU_CONTRACT_CREATION and choice != MENU_CONTRACT_UPDATE and\
            choice != MENU_CONTRACT_DELETE and choice != MENU_CONTRACT_EXIT and\
            choice != MENU_CONTRACT_SIGNATURE:
            clear_screen()
            print("+--------------------------------+")
            print("|          MENU CONTRAT          |")
            print("+--------------------------------+")
            print("| 1 - création d'un contrat      |")
            print("| 2 - voir/modifier un contrat   |")
            print("| 3 - suppression d'un contrat   |")
            print("| 4 - signer un contrat          |")
            print("| 5 - revenir au menu principal  |")
            print("+--------------------------------+")

            choice = input("Quel est votre choix : ")
            if not choice.isnumeric():
                print("Merci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)

        return choice

    def add_contract(self):
        """ ask informations about new contract to add """

        clear_screen()
        price, due = None, None
        
        customer_info = input("Information sur le client et sur l'evenement (max 5000 caractères) : ")

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
                    print("\nLe montant du ne peut pas etre superieur au montant du contrat.\n")
                else:
                    break

            while True:
                status = input("Contrat signé (o)ui/(n)on ([ENTRER] = non): ")
                if not status.lower() == "o" and not status.lower() == "n" and not status == "":
                    print("\nSaisie incorrect, reessayez svp.\n")
                elif status == "" or status.lower() == "n":
                    status = "NOT-SIGNED"
                    break
                else:
                    status = "SIGNED"
                    break
            
            return customer_info, price, due, status

    def select_contract_by_entry(self):
        """ selection of a contract by typing """

        while True:
            contract_number = input("\nQuel est le numero du contrat ([ENTRER] pour afficher une liste)? ")
            print()
            if not contract_number:
                return None
            elif not contract_number.isnumeric():
                print("\nMerci de saisir un chiffre.\n")
            else:
                print()
                return contract_number
    
    def select_contract_by_list(self, contracts_list):
        """ selection of a contract by list """

        # display list of contracts
        while True:
            counter_int = 1

            for contract in contracts_list:
                print(str(counter_int) + " - " + str(contract))
                counter_int += 1
                time.sleep(0.1)
                if counter_int %5 == 0:
                    choice = input("\nQuel est votre choix ([ENTRER] pour continuer ou (q)uitter)? ")
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

            choice = input("\nFin de liste atteinte. Faites un choix ou [ENTRER] pour relancer ou (q)uitter: ")
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
        """ modifications input for a contract """    

        clear_screen()
        print("\nContrat selectionné :", contract_obj)
        print()

        # view and modify value for an contract
        customer_info = None
        modification_state_boolean = False

        print(f"Information actuelle sur le client et son evenement:\n{contract_obj.customer_info}\n")
        customer_info = input("Modifier ([ENTRER] pour conserver information actuelle)? ")
        if customer_info:
            modification_state_boolean = True
            contract_obj.customer_info = customer_info

        while True:
            price = input(f"Prix actuel : '{contract_obj.price}' [ENTRER pour conserver prix actuel]: ")
            if price.isnumeric():
                modification_state_boolean = True
                contract_obj.price = price
                break
            elif not price:
                break
            else:
                print("\nMerci de préciser un prix en chiffre...\n")

        while True:
            print(f"Montant restant du actuel : '{contract_obj.due}")
            due = input(f"Preciser nouveau montant (<{contract_obj.price}) [ENTRER pour conserver montant actuel]: ")
            if due.isnumeric():
                modification_state_boolean = True
                contract_obj.due = due
                break
            elif not due:
                break
            elif int(due) > int(price):
                print("\nLe montant du ne peut pas etre superieur au montant du contrat.\n")
            else:
                print("\nMerci de préciser un montant en chiffre...\n")
        
        while True:
            status = input("Signer contrat? (o/N): ")
            if not status.lower() == "o" and not status.lower() == "n" and not status == "":
                print("\nSaisie incorrect, reessayez svp.\n")
            elif status == "" or status.lower() == "n":
                status = "NOT-SIGNED"
                break
            else:
                status = "SIGNED"
                break
        
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
            if not status.lower() == "o" and not status.lower() == "n" and not status == "":
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
        print(f"* Information      : {contract_obj.customer_info}")
        input("\n[ENTRER] pour retourner au menu.\n")
    