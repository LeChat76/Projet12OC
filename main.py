from controllers.base import epicEvents
from models.database_model import DatabaseModel
from constants.database import DB_URL


def main():
    """ Launching start here """

    db = DatabaseModel(DB_URL)
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
