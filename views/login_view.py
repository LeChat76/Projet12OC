from getpass_asterisk.getpass_asterisk import getpass_asterisk
import time


class LoginMenu:
    """ Login class """

    def login_menu(self, show_title):
        """ Login Menu """

        if show_title == True:
            title = (
            " ______       _         ______               _       ",
            "|  ____|     (_)       |  ____|             | |      ",
            "| |__   _ __  _  ___   | |____   _____ _ __ | |_ ___ ",
            "|  __| | '_ \| |/ __|  |  __\ \ / / _ \ '_ \| __/ __|",
            "| |____| |_) | | (__   | |___\ V /  __/ | | | |_\__ \ ",
            "|______| .__/|_|\___|  |______\_/ \___|_| |_|\__|___/",
            "       | |",
            "       |_|"
        )
            for line_title in title:
                print(line_title)
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
