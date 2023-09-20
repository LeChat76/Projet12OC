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
                break
            except ValueError:
                print("\nFormat de date incorrect. Merci de resaisir.")
        
        while True:
            date_end = input("\nQuel est la date de fin de l'évènement (exemple 04/06/23 13:00)? ")
            # A SUPPRIMER =================
            if not date_end:
                date_end="05/06/23 14:00"
            # =============================
            try:
                datetime.strptime(date_end, date_format)
                if date_end <= date_start:
                    print("\nLa date de fin doit être forcement supérieure à la date de début. Merci de resaisir.")
                else:
                    break
            except ValueError:
                print("\nFormat de date incorrect. Merci de resaisir.")
        
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




