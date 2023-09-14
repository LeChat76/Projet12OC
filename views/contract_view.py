import time
from views.utils_view import clear_screen
from models.models import ContractModel
from views.customer_view import CustomerView
from models.models import CustomerModel, EmployeeModel
from constants.contract_menu import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_DELETE, MENU_CONTRACT_SIGNATURE, MENU_CONTRACT_EXIT


class ContractView:
    """ Customer view class """

    def __init__(self):
        self.customer_view = CustomerView()
        self.employee_model = EmployeeModel()
        self.contract_model = ContractModel(None, None, None, None, None, None)
        self.customer_model = CustomerModel(None, None, None, None, None)

    def contract_menu(self):
        """ Menu 2 - CONTRAT """

        choice = None
        while choice !=  MENU_CONTRACT_CREATION and choice != MENU_CONTRACT_UPDATE and\
            choice != MENU_CONTRACT_DELETE and choice != MENU_CONTRACT_EXIT and\
            choice != MENU_CONTRACT_SIGNATURE:
            clear_screen()
            print("+-------------------------------+")
            print("|          MENU CONTRAT         |")
            print("+-------------------------------+")
            print("| 1 - création d'un contrat     |")
            print("| 2 - voir/modifier un contrat  |")
            print("| 3 - suppression d'un contrat  |")
            print("| 4 - signer un contrat         |")
            print("| 5 - revenir au menu principal |")
            print("+-------------------------------+")

            choice = input("Quel est votre choix : ")
            if not choice.isnumeric():
                print("Merci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)
        clear_screen()

        return choice

    def add_contract(self, employee_id):
        """ ask informations about new contract to add """

        clear_screen()
        price, due = None, None
        
        customer_info = input("Information sur le client et sur l'evenement (max 5000 caractères) : ")

        while True:

            while True:
                price = input('Prix [ENTRER = 0€] : ')
                if price == '':
                    price = 0
                    break
                elif not price.isnumeric() and not price == '':
                    print('\nMerci de renseigner uniquement des chiffres.\n')
                else:
                    break
            
            while True:
                due = input(f"Montant restant du (< à {price}, [ENTRER = 0€] : ")
                if due == '':
                    due = 0
                    break
                elif not due.isnumeric() and not due == '':
                    print('\nMerci de renseigner uniquement des chiffres.\n')
                elif int(due) > int(price):
                    print('\nLe montant du ne peut pas etre superieur au montant du contrat.\n')
                else:
                    break

            while True:
                status = input('Contrat signé (o)ui / (n)on [ENTRER = non] : ')
                if not status.lower() == 'o' and not status.lower() == 'n' and not status == '':
                    print('\nSaisie incorrect, reessayez svp.\n')
                elif status == '' or status.lower() == 'n':
                    status = 'NOT-SIGNED'
                    break
                else:
                    status = 'SIGNED'
                    break
            
            customer_choice = self.customer_view.select_customer_by_entry()
            if customer_choice.lower() == 'q':
                return 'q'
            else:
                customer_obj = self.customer_model.create_customer_object(customer_choice)
                new_contract = ContractModel(customer_info, price, due, status, customer_obj, employee_id)
                return new_contract

    def select_contract_by_entry(self):
        """ selection of a contract by typing """

        while True:
            contract_number = input('Quel est le numero du contrat ([ENTRER] pour afficher une liste)? ')
            if not contract_number:
                contract = self.select_contract_by_list()
                return contract
            elif not contract_number.isnumeric():
                print("\nMerci de saisir un chiffre.\n")
            else:
                return contract_number
    
    def select_contract_by_list(self):
        """ selection of a contract by list """

        # display list of contracts
        list_contracts = self.contract_model.search_all_contracts()
        while True:
            counter = 1
            contract_id_list = []
            choice_made = False

            for contract in list_contracts:
                print(" - " + str(contract))
                contract_id_list.append(contract.id)
                counter += 1
                time.sleep(0.1)
                if counter %5 == 0:
                    choice = input ('\nAvez vous fait un choix [ENTRER] pour continuer ou (q)uitter? ')
                    print()
                    if choice.lower() == 'q':
                        choice_made = True
                        break
                    elif choice:
                        choice_made = True
                        break

            if not choice_made:
                choice = input('\nFin de liste atteint. Faites un choix, [ENTRER] pour relancer ou (q)uitter? ')
                print()
                if choice.lower() == 'q':
                    return choice
                elif choice:
                    choice_made = True
                    return choice
            else:
                return choice
        
    def modify_contract(self, contract):
        """ modifications input for a contract """    

        clear_screen()
        print('\nContrat selectionné :', contract)
        print()

        # view and modify value for an contract
        customer_info = None
        modification_state = False

        print(f"Information actuelle sur le client et son evenement :\n {contract.customer_info}\n")
        customer_info = input("Modifier ([ENTRER] pour conserver information actuelle)? ")
        if customer_info:
            modification_state = True
            contract.customer_info = customer_info

        while True:
            price = input(f"Prix actuel : '{contract.price}' [ENTRER pour conserver prix actuel]: ")
            if price.isnumeric():
                modification_state = True
                contract.price = price
                break
            elif not price:
                break
            else:
                print("\nMerci de préciser un prix en chiffre...\n")

        while True:
            print(f"Montant restant du actuel : '{contract.due}")
            due = input(f"Preciser nouveau montant (<{contract.price}) [ENTRER pour conserver montant actuel]: ")
            if due.isnumeric():
                modification_state = True
                contract.due = due
                break
            elif not due:
                break
            elif int(due) > int(price):
                print('\nLe montant du ne peut pas etre superieur au montant du contrat.\n')
            else:
                print("\nMerci de préciser un montant en chiffre...\n")
        
        while True:
            status = input("Signer contrat? (o/N): ")
            if not status.lower() == 'o' and not status.lower() == 'n' and not status == '':
                print('\nSaisie incorrect, reessayez svp.\n')
            elif status == '' or status.lower() == 'n':
                status = 'NOT-SIGNED'
                break
            else:
                status = 'SIGNED'
                break
        
        if modification_state:
            #record modifications in database
            self.contract_model.update_contract(contract)
        else:
            print('\nAucune modification apportée au contrat, retour au menu.\n')
            time.sleep(3)

    def sign_contract(self, contract):
        """
        sign contract method
        INPUT : contract object
        OUTPUT : contract.status=SIGNED
        """

        clear_screen()
        print('\nContrat selectionné :', contract)
        print()

        contract.status = "SIGNED"
        self.contract_model.update_contract(contract)
        

    def display_contract_informations(self, contract):
        """
        display contract information
        INPUT : contract object
        RESULT : displaying contract informations
        """

        print("\nVos droits ne vous donne accès qu'en lecture.\n")
        print(f'* Numéro           : {contract.id}')
        print(f'* Prix             : {contract.price}')
        print(f'* Due              : {contract.due}')
        print(f'* Status           : {contract.status}')
        print(f'* Information      : {contract.customer_info}')
        input('\n[ENTRER] pour retourner au menu.\n')
    