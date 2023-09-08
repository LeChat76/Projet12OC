from controllers.base import epicEvents, BaseController
from constants import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


def main():
    """
    Launching starti here.
    First : create Tables for first launch
    Then : launch Epic Events login menu
    """
    db_url = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    controller = BaseController(db_url)
    if not controller.db.tables_exist():
       controller.initialize()

    epicevents = epicEvents(controller.db)
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
