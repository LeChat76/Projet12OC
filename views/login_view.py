from getpass_asterisk.getpass_asterisk import getpass_asterisk
import time


class LoginMenu:
    """ Login class """

    def login_menu(self, show_title):
        """ Login Menu """

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
            print("       |_|\n")
            time.sleep(0.1)

        username = input("Nom d'utilisateur : ")
        if not username:
            # A SUPPRIMER
            username = 'cedric'
        password = getpass_asterisk('Mot de passe : ')
        if not password:
            # A SUPPRIMER
            password = 'Toto1234!'

        return username, password
