import re
import time
from views.utils_view import clear_screen
from constants.customer import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT
from models.models import CustomerModel


class CustomerView:
    """ Customer view class """

    def __init__(self):
        self.customer_model = CustomerModel(None, None, None, None, None)

    def customer_menu(self):
        """ Menu 1 - CLIENT """

        choice = None
        while choice !=  MENU_CUSTOMER_CREATION and choice != MENU_CUSTOMER_UPDATE and\
            choice != MENU_CUSTOMER_DELETE and choice != MENU_CUSTOMER_EXIT:
            clear_screen()
            print("+-------------------------------+")
            print("|          MENU JOUEUR          |")
            print("+-------------------------------+")
            print("| 1 - création d'un client      |")
            print("| 2 - voir/modifier un client   |")
            print("| 3 - suppression d'un client   |")
            print("| 4 - revenir au menu principal |")
            print("+-------------------------------+")

            choice = input("Quel est votre choix : ")
            if not choice.isnumeric():
                print("Merci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)

        return choice
    
    def add_customer(self, employee_obj):
        """ ask informations about new customer to add """

        customer_name, customer_email, customer_phone, customer_company = None, None, None, None
        
        while not customer_name:
            customer_name = input("\nNom du client (obligatoire, max 255 caractères): ")
        
        while not customer_email:
            customer_email = input("Email du client (obligatoire, max 255 caractères): ")
            if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", customer_email):
                break
            else:
                customer_email = None
                print("\nL'adresse e-mail n'est pas valide. Veuillez réessayer.\n")
        
        while not customer_phone:
            customer_phone = input("Numero de telephone du client (facultatif, max 20 caractères): ")
            if re.match(r"^[0-9+\-]+( [0-9+\-]+)*$", customer_phone):
                break
            elif customer_phone == "":
                break
            else:
                customer_phone = None
                print("\nLe numéro de téléphone n'est pas valide. Veuillez réessayer.\n")
        
        while not customer_company:
            customer_company = input("Nom de l'entreprise (obligatoire, max 255 caractères): ")
        
        new_customer_obj = CustomerModel(customer_name, customer_email, customer_phone, customer_company, employee_obj)

        return new_customer_obj
    
    def select_customer_by_entry(self):
        """ selection of a customer by typing """

        while True:
            customer_name = input("\nQuel est le nom du client [ENTRER pour afficher une liste]? ")
            print()
            if not customer_name:
                customer = self.select_customer_by_list()
                return customer
            elif any(char.isalpha() for char in customer_name) and any(char.isdigit() for char in customer_name):
                return customer_name
            elif any(char.isalpha() for char in customer_name):
                return customer_name                
    
    def select_customer_by_list(self):
        """ selection of a customer by list """

        # display list of customers
        customers_list = self.customer_model.search_all_customers()
        while True:
            counter_int = 1
            customer_id_list = []
            choice_made_boolean = False

            for customer in customers_list:
                print(str(counter_int) + ' - ' + str(customer))
                customer_id_list.append(customer.id)
                counter_int += 1
                time.sleep(0.1)
                if counter_int %5 == 0:
                    choice = input ("\nSaisir numero de ligne ou [ENTRER] pour continuer ou (q)uitter? ")
                    if choice.lower() == "q":
                        choice_made_boolean = True
                        break
                    elif choice:
                        choice_made_boolean = True
                        break
                    else:
                        print()

            if not choice_made_boolean:
                choice = input("\nFin de liste atteinte. Faites un choix, [ENTRER] pour relancer ou (q)uitter? ")
                print()
                if choice.lower() == "q":
                    return choice
                elif choice:
                    choice_made_boolean = True
                    return choice
            else:
                return choice
        
    def modify_customer(self, customer):
        """ modifications input for a customer """    

        clear_screen()
        print("\nClient selectionné :", customer)
        print()

        # view and modify value in customer
        customer_name, customer_email, customer_phone, customer_company = None, None, None, None
        modification_state_boolean = False

        while True:
            customer_name = input(f"Nom du client '{customer.name}' [ENTRER pour conserver actuel]: ")
            if customer_name:
                modification_state_boolean = True
                customer.name = customer_name
                break
            else:
                break

        while True:
            customer_email = input(f"Email du client '{customer.email}' [ENTRER pour conserver actuel]: ")
            if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", customer_email):
                modification_state_boolean = True
                customer.email = customer_email
                break
            elif not customer_email:
                break
            else:
                print("\nL'adresse e-mail n'est pas valide. Veuillez resaisir.\n")

        while True:
            customer_phone = input(f"Numero de telephone du client '{customer.phone}' [ENTRER pour conserver actuel]: ")
            if re.match(r"^[0-9+\-]+( [0-9+\-]+)*$", customer_phone):
                modification_state_boolean = True
                customer.phone = customer_phone
                break
            elif not customer_phone:
                break
            else:
                print("\nLe numéro de téléphone n'est pas valide. Veuillez resaisir.\n")
        
        while True:
            customer_company = input(f"Nom de la société du client '{customer.company}' [ENTRER pour conserver actuel]: ")
            if customer_company:
                modification_state_boolean = True
                customer.company = customer_company
                break
            else:
                break
        
        if modification_state_boolean:
            #record modifications in database
            self.customer_model.update_customer(customer)
        else:
            print("\nAucune modification apportée au client, retour au menu.\n")
            time.sleep(3)

    def display_customer_informations(self, customer):
        """
        display customer information
        INPUT : customer object
        RESULT : display customer informations
        """

        print("\nVos droits ne vous donne accès qu'en lecture.\n")
        print(f"* Nom              : {customer.name}")
        print(f"* Email            : {customer.email}")
        print(f"* Societe          : {customer.company}")
        print(f"* Telephone        : {customer.phone}")
        print(f"* Date de creation : {customer.date_creation}")
        input("\n[ENTRER] pour retourner au menu.\n")
    