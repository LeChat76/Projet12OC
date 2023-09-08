import time
from views.utils_view import clear_screen
from constants import MENU_CLIENTS, MENU_CONTRATS, MENU_EVENEMENTS, MENU_EXIT


class LoginMenu:
    
    def login_menu(self, show_title):
        """ LOGIN Menu """

        if show_title == True:
            print(" ______       _         ______               _       ")
            time.sleep(0.1)
            print("|  ____|     (_)       |  ____|             | |      ")
            time.sleep(0.1)
            print("| |__   _ __  _  ___   | |____   _____ _ __ | |_ ___ ")
            time.sleep(0.1)
            print("|  __| | '_ \| |/ __|  |  __\ \ / / _ \ '_ \| __/ __|")
            time.sleep(0.1)
            print("| |____| |_) | | (__   | |___\ V /  __/ | | | |_\__ \ ")
            time.sleep(0.1)
            print("|______| .__/|_|\___|  |______\_/ \___|_| |_|\__|___/")
            time.sleep(0.1)
            print("       | |")
            time.sleep(0.1)
            print("       |_|")
            time.sleep(0.1)

        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")

        return username, password
