from views.utils_view import clear_screen
from models.models import ContractModel
from views.customer_view import CustomerView
from models.models import CustomerModel
from constants.contract_menu import MENU_CONTRACT_CREATION, MENU_CONTRACT_UPDATE, MENU_CONTRACT_DELETE, MENU_CONTRACT_SIGNATURE, MENU_CONTRACT_EXIT


class ContractView:
    """ Customer view class """

    def __init__(self):
        self.customer_view = CustomerView()
        self.contract_model = ContractModel(None, None, None, None, None)
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

    def add_contract(self):
        """ ask informations about new contract to add """

        clear_screen()
        price, due = None, None
        
        customer_info = input('Information sur le client (max 5000 caractères) : ')

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
                due = input('Montant restant du [ENTRER = 0€] : ')
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
                status = input('Contrat signé : (o)ui / (n)on [ENTRER = non]')
                if not status.lower() == 'o' and not status.lower() == 'n' and not status == '':
                    print('\nSaisie incorrect, reessayez svp.\n')
                elif status.lower() == '' or status.lower() == 'n':
                    status = 'NOT-SIGNED'
                    break
                else:
                    status = 'SIGNED'
                    break
            
            customer_choice = self.customer_view.select_customer_by_entry()
            if customer_choice.lower() == 'q':
                return 'q'
                break
            else:
                customer = self.customer_model.create_customer_object(customer_choice)
                new_contract = ContractModel(customer_info, price, due, status, customer)
                return new_contract