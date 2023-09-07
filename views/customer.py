import os
from constants import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT
from models.models import Customer


class CustomerView:
    """ Menu CUSTOMER """

    def player_menu(self):
        """ Menu 1 """
        choix = None
        while choix !=  MENU_CUSTOMER_CREATION and choix != MENU_CUSTOMER_UPDATE and choix != MENU_CUSTOMER_DELETE and\
                choix != MENU_CUSTOMER_EXIT:
            # self.clear_screen()
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
        # self.clear_screen()
        return choix
    
    def add_customer(self):
        """ Method to ask informations about new customer to add """
        # self.clear_screen()
        customer_name, customer_email, customer_phone, customer_company = None, None, None, None
        
        while not customer_name:
            customer_name = input('Nom du client (obligatoire, max 255 caractères): ')
        
        while not customer_email:
            customer_email = input('Email du client (obligatoire, max 255 caractères): ')
        
        customer_phone = input('Numero de telephone du client (facultatif, max 20 caracères): ')
        
        while not customer_company:
            customer_company = input("Nom de l'entreprise (obligatoire, max 255 caractères): ")
        
        new_customer = Customer(customer_name, customer_email, customer_phone, customer_company, '1')

        return new_customer


        



        



    def clear_screen(self):
        if os.name == "posix":
            os.system("clear")
        elif os.name == "nt":
            os.system('cls')