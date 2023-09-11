import re
import time
from views.utils_view import clear_screen
from constants.customer_menu import MENU_CUSTOMER_CREATION, MENU_CUSTOMER_UPDATE, MENU_CUSTOMER_DELETE, MENU_CUSTOMER_EXIT
from models.models import Customer
from models.customer_model import CustomerModel


class CustomerView:
    """ Customer view class """

    def __init__(self):
        self.customer_model = CustomerModel()

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
            print("| 2 - voir/modifier un client   |")
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
        """ ask informations about new customer to add """

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
    
    def select_customer(self, employee):
        """ update informations about customer """

        clear_screen()
        while True:
            customer_name = input('Quel est le nom du client [ENTRER pour afficher une liste]? ')
            if not customer_name:
                customer = self.select_customer_by_list(employee)
                return customer
            elif any(char.isalpha() for char in customer_name) and any(char.isdigit() for char in customer_name):
                return customer_name
                
            elif any(char.isalpha() for char in customer_name):
                return customer_name                

    
    def select_customer_by_list(self, employee):
        """ display customers associated to an employee """

        # display list
        clear_screen()
        list_customers = self.customer_model.search_customer(employee)
        while True:
            counter = 1
            choice_made = False

            for customer in list_customers:
                print(str(counter) + ' - ' + str(customer))
                counter += 1
                time.sleep(0.1)
                if counter %5 == 0:
                    choice = input ('\nAvez vous fait un choix [ENTER pour continuer]? ')
                    print()
                    if choice:
                        choice_made = True
                        break

            if not choice_made:
                choice = input('\nLa liste est terminée. [ENTRER] pour relancer la liste ou (q)uitter? ')
                print()
                if choice.lower() == 'q':
                    break
            else:
                return choice
        
    def modify_customer(self, customer_choice, permission):
        """ display modifications input for a customer """    

        # extract customer data from database
        customer = self.customer_model.select_customer(customer_choice)

        if permission:
            print('\nClient selectionné :', customer)
            print()

            # view and modify value in customer
            customer_name, customer_email, customer_phone, customer_company = None, None, None, None
            modification_state = False


            while True:
                customer_name = input(f"Nom du client '{customer.name}' [ENTRER pour conserver actuel]: ")
                if customer_name:
                    modification_state = True
                    customer.name = customer_name
                    break
                else:
                    break

            while True:
                customer_email = input(f"Email du client '{customer.email}' [ENTRER pour conserver actuel]: ")
                if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", customer_email):
                    modification_state = True
                    customer.email = customer_email
                    break
                elif not customer_email:
                    break
                else:
                    print("\nL'adresse e-mail n'est pas valide. Veuillez réessayer.\n")

            while True:
                customer_phone = input(f"Numero de telephone du client '{customer.phone}' [ENTRER pour conserver actuel]: ")
                if re.match(r"^[0-9+\-]+( [0-9+\-]+)*$", customer_phone):
                    modification_state = True
                    customer.phone = customer_phone
                    break
                elif not customer_phone:
                    break
                else:
                    print("\nLe numéro de téléphone n'est pas valide. Veuillez réessayer.\n")
            
            while True:
                customer_company = input(f"Nom de la société du client '{customer.company}' [ENTRER pour conserver actuel]: ")
                if customer_company:
                    modification_state = True
                    customer.company = customer_company
                    break
                else:
                    break
            
            if modification_state:
                #record modifications in database
                self.customer_model.update_customer(customer)
            else:
                print('\nAucune modification apportée au client, retour au menu.\n')
                time.sleep(2)
        else:
            print('\nVotre autorisation ne vous permet que de voir les informations clients.\n')
            print(f'Nom              : {customer.name}')
            print(f'Email            : {customer.email}')
            print(f'Societe          : {customer.company}')
            print(f'Telephone        : {customer.phone}')
            print(f'Date de creation : {customer.date_creation}\n')
            input('[ENTRER] pour retourner au menu.\n')
    
    def delete_customer(self, customer):
        """ display the customer deletion menu """

        




