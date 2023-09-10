from utils.utils import clear_screen, check_permission
from constants.constants import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT
from models.models import Customer
import re


class CustomerView:

    def customer_menu(self):
        """ Menu 1 """
        choix = None
        while choix !=  MENU_CUSTOMER_CREATION and choix != MENU_CUSTOMER_UPDATE and choix != MENU_CUSTOMER_DELETE and\
                choix != MENU_CUSTOMER_EXIT:
            clear_screen()
            print("+-------------------------------+")
            print("|          MENU JOUEUR          |")
            print("+-------------------------------+")
            print("| 1 - création d'un client      |")
            print("| 2 - mettre à jour un client   |")
            print("| 3 - suppression d'un client   |")
            print("| 4 - revenir au menu principal |")
            print("+-------------------------------+")
            choix = input("Quel est votre choix : ")
            if not choix.isnumeric():
                print("Merci de préciser un choix numérique.")
                choix = None
            else:
                choix = int(choix)
        clear_screen()
        return choix
    
    def add_customer(self, employee):
        """ Method to ask informations about new customer to add """

        customer_name, customer_email, customer_phone, customer_company = None, None, None, None
        
        while not customer_name:
            customer_name = input('Nom du client (obligatoire, max 255 caractères): ')
        
        while not customer_email:
            customer_email = input('Email du client (obligatoire, max 255 caractères): ')
            if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", customer_email):
                break
            else:
                customer_email = None
                print("\nL'adresse e-mail n'est pas valide. Veuillez réessayer.\n")
        
        while not customer_phone:
            customer_phone = input('Numero de telephone du client (facultatif, max 20 caracères): ')
            if re.match(r"^[0-9+\-]+( [0-9+\-]+)*$", customer_phone):
                break
            elif customer_phone == '':
                break
            else:
                customer_phone = None
                print("\nLe numéro de téléphone n'est pas valide. Veuillez réessayer.\n")
        
        while not customer_company:
            customer_company = input("Nom de l'entreprise (obligatoire, max 255 caractères): ")
        
        new_customer = Customer(customer_name, customer_email, customer_phone, customer_company, employee.id)

        return new_customer
    
    def update_customer(self, employee):
        """ Method to update informations about new customer to add """

        clear_screen()
        permission = check_permission('commercial', employee)
        if permission:
            customer = input('Quel est le nom du client à modifier [ENTRER pour afficher une liste]? ')
            if not customer:
                pass
            else:
                pass
        
