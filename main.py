from controllers.base import epicEvents
from models.database_model import DatabaseModel
from constants.database import DB_URL
from constants.sentry import DSN
from utils.utils_sentry import send_to_sentry
import sentry_sdk


def main():
    """ Launching start here """

    sentry_sdk.init(
        dsn=DSN,
        traces_sample_rate=1.0,
    )

    db = DatabaseModel(DB_URL)
    epicevents = epicEvents()

    try:
        epicevents.login_menu()
    except KeyboardInterrupt as e:
        send_to_sentry("application", "interrupt", e)
        print("\n\nFin du script par l'utilisateur.\n")
    finally:
        if db:
            print('Fermeture de la session MySql\n')
            db.get_session().close()

if __name__ == "__main__":
    main()
