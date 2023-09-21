from views.utils_view import clear_screen
from constants.event import MENU_EVENT_CREATION, MENU_EVENT_ASSIGNATION,MENU_EVENT_UPDATE,MENU_EVENT_DELETE, MENU_EVENT_EXIT
from datetime import datetime
import re, time


class EventView:
    """ Event view class """

    def event_menu(self):
        """ Menu 3 - EVENT """

        choice = None
        while choice !=  MENU_EVENT_CREATION and choice != MENU_EVENT_UPDATE and\
            choice != MENU_EVENT_DELETE and choice != MENU_EVENT_EXIT and\
            choice != MENU_EVENT_ASSIGNATION:
            clear_screen()
            print("+--------------------------------+")
            print("|        MENU EVENEMENT          |")
            print("+--------------------------------+")
            print("| 1 - création d'un evenement    |")
            print("| 2 - assignation d'un evenement |")
            print("| 3 - voir/modifier un evenement |")
            print("| 4 - suppression d'un evenement |")
            print("| 5 - revenir au menu principal  |")
            print("+--------------------------------+")

            choice = input("Quel est votre choix : ")
            if not choice.isnumeric():
                print("Merci de préciser un choix numérique.")
                choice = None
            else:
                choice = int(choice)

        return choice

    def add_event(self):
        """ ask informations about new event to create """

        date_format = "%d/%m/%y %H:%M"
        location_pattern = r'^\s*[A-Za-zÀ-ÿ0-9\s]*\s*,\s*[0-9]{5}\s*,\s*[A-Za-zÀ-ÿ\s]*\s*$'
        notes = None

        while True:
            date_start = input("Quel est la date de début de l'évènement (exemple 04/06/23 13:00)? ")
            # A SUPPRIMER =================
            if not date_start:
                date_start="04/06/23 13:00"
            # =============================
            try:
                datetime.strptime(date_start, date_format)
                date_start = datetime.strptime(date_start, date_format)
                break
            except ValueError:
                print("\nFormat de date incorrect. Merci de resaisir.\n")
        
        while True:
            date_end = input("\nQuel est la date de fin de l'évènement (exemple 04/06/23 13:00)? ")
            # A SUPPRIMER =================
            if not date_end:
                date_end="05/06/23 14:00"
            # =============================
            try:
                datetime.strptime(date_end, date_format)
                date_end = datetime.strptime(date_end, date_format)
                if date_end <= date_start:
                    print("\nLa date de fin doit être forcement supérieure à la date de début. Merci de resaisir.")
                else:
                    break
            except ValueError:
                print("\nFormat de date incorrect. Merci de resaisir.\n")
        
        while True:
            location = input("\nQuel est le lieu de l'évènement (exemple : 97 Allée des Platanes, 76520, Boos)? ")
            # A SUPPRIMER =================
            if not location:
                location="97 Allée des Platanes, 76520, Boos"
            # =============================
            if re.match(location_pattern, location):
                break
            else:
                print("\nFormat d'adresse incorrect, merci de suivre le format : [rue], [code_postal], [ville].")
        
        while True:
            attendees = input("\nCombien d'invités? ")
            # A SUPPRIMER =================
            if not attendees:
                attendees="75"
            # =============================
            if not attendees.isnumeric():
                print("\nMerci de préciser un nombre.")
            else:
                if int(attendees)==0:
                    print("\nLe nombre d'invités doit être supérieur à 0.")
                else:
                    break
        
        notes = input("\nNotes: ")

        return date_start, date_end, location, attendees, notes

    def select_event_by_entry(self):
        """ selection of an event by typing """

        while True:
            event_number = input("\nQuel est le numero de l'evenement [ENTRER pour afficher une liste]? ")
            if not event_number:
                print()
                return None
            elif not event_number.isnumeric():
                print("\nMerci de saisir un chiffre.\n")
            else:
                print()
                return event_number

    def select_event_by_list(self, events_list):
        """ selection of a customer by list """

        while True:
            counter_int = 1
            event_id_list = []

            for event in events_list:
                print(str(counter_int) + ' - ' + str(event))
                event_id_list.append(event.id)
                counter_int += 1
                time.sleep(0.1)
                if counter_int %5 == 0:
                    choice = input ("\nSaisir numero de ligne ([ENTRER] pour continuer ou (q)uitter)? ")
                    if choice.lower() == "q":
                        return choice
                    elif choice.isalpha():
                        print("\nMerci de saisir un chiffre.\n")
                    elif choice.isnumeric():
                        if int(choice) >= counter_int:
                            print("\nCe choix ne fait pas parti de la liste...\n")
                        else:
                            return choice
                    else:
                        print()

            choice = input("\nFin de liste atteinte. Faites un choix ou [ENTRER] pour relancer ou (q)uitter: ")
            if choice.lower() == "q":
                return choice
            elif choice.isalpha():
                print("\nMerci de saisir un chiffre.\n")
            elif choice.isnumeric():
                if int(choice) >= counter_int:
                    print("\nCe choix ne fait pas parti de la liste...\n")
                else:
                    return choice

    def display_event_informations(self, event_obj, customer_obj, employee_obj):
        """
        display event informations
        INPUT : event object + customer object + employee_obj
        RESULT : display event informations
        """

        print("\nVos droits ne vous donne accès qu'en lecture.\n")
        if event_obj.contract_id:
            print(f"* Contrat          : {event_obj.contract_id}")
        print(f"* Client           : {customer_obj.name}")
        print(f"* Email            : {customer_obj.email}")
        if customer_obj.phone:
            print(f"* Telephone        : {customer_obj.phone}")
        print(f"* Début            : {event_obj.date_start}")
        print(f"* Fin              : {event_obj.date_end}")
        if employee_obj:
            assigned_employee = employee_obj.username
        else:
            assigned_employee = "pas encore assigné"
        print(f"* Assigné à        : {assigned_employee}")
        print(f"* Adresse          : {event_obj.location}")
        print(f"* Information      : {event_obj.notes}")
        input("\n[ENTRER] pour retourner au menu.\n")

    def update_event(self, event_obj):
        """ ask informations for update existing event """

        clear_screen()
        print("\nEvenement selectionné :", event_obj)
        print()

        modification_state_boolean = False
        date_format = "%d/%m/%y %H:%M"
        location_pattern = r'^\s*[A-Za-zÀ-ÿ0-9\s]*\s*,\s*[0-9]{5}\s*,\s*[A-Za-zÀ-ÿ\s]*\s*$'
        notes = None

        while True:
            date_start = input(f"\nDate de depart actuelle '{event_obj.date_start.strftime(date_format)}' ([ENTRER] pour conserver): ")
            if not date_start:
                break
            else:
                try:
                    datetime.strptime(date_start, date_format)
                    event_obj.date_start = date_start
                    break
                except ValueError:
                    print("\nFormat de date incorrect. Merci de resaisir.\n")
        
        while True:
            event_date_start = event_obj.date_start
            date_end = input(f"\nDate de fin actuelle '{event_obj.date_end.strftime(date_format)}' ([ENTRER] pour conserver): ")
            if not date_end:
                break
            else:
                try:
                    datetime.strptime(date_end, date_format)
                    if date_end <= event_date_start:
                        print("\nLa date de fin doit être forcement supérieure à la date de début. Merci de resaisir.")
                    else:
                        modification_state_boolean = True
                        event_obj.end_date = date_end
                        break
                except ValueError:
                    print("\nFormat de date incorrect. Merci de resaisir.\n")
        
        while True:
            location = input(f"\nLieu actuel '{event_obj.location}' ? ([ENTRER] pour conserver): ")
            if not location:
                break
            elif re.match(location_pattern, location):
                modification_state_boolean = True
                event_obj.location = location
                break
            else:
                print("\nFormat d'adresse incorrect, merci de suivre le format : [rue], [code_postal], [ville].")
        
        while True:
            attendees = input(f"\nNombre d'invités actuel '{event_obj.attendees}' ([ENTRER] pour conserver): ")
            if not attendees:
                break
            elif not attendees.isnumeric():
                print("\nMerci de préciser un nombre.")
            else:
                if int(attendees)==0:
                    print("\nLe nombre d'invités doit être supérieur à 0.")
                else:
                    modification_state_boolean = True
                    event_obj.attendees = attendees
                    break
        
        while True:
            notes = input(f"\nNotes actuelles '{event_obj.notes}' ([ENTRER] pour conserver): ")
            if notes:
                modification_state_boolean = True
                event_obj.notes = notes
                break
            else:
                break

        if modification_state_boolean:
            return event_obj
        else:
            return None




