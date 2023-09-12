from controllers.base import epicEvents
from models.models import Database
from constants.database_config import DB_URL


def main():
    """ Launching start here """

    db = Database(DB_URL)
    epicevents = epicEvents()

    try:
        epicevents.login_menu()
    except KeyboardInterrupt:
        print("\n\nFin du script par l'utilisateur.\n")
    finally:
        if db:
            print('Fermeture de la session MySql\n')
            db.get_session().close()

if __name__ == "__main__":
    main()
