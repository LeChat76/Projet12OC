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
            print("       |_|")
            time.sleep(0.1)

        while True:
            username = getpass_asterisk("\nNom d'utilisateur : ")
            if not username:
                print("\nMerci de sair un nom d'utilisateur...")
            else:
                break
        while True:
            password = getpass_asterisk("\nMot de passe : ")
            if not password:
                print("\nMerci de sair un mot de passe...")
            else:
                break

        return username, password
