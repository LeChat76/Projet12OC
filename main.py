from controllers.base import epicEvents, BaseController
from constants.constants import DB_URL


def main():
    """ Launching start here """

    controller = BaseController(DB_URL)
    epicevents = epicEvents()

    try:
        epicevents.login_menu()
    except KeyboardInterrupt:
        print("\n\nFin du script par l'utilisateur.\n")
    finally:
        if controller.db:
            print('Fermeture de la session MySql\n')
            controller.db.get_session().close()

if __name__ == "__main__":
    main()
