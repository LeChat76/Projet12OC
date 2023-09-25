from controllers.base import epicEvents
from models.database_model import DatabaseModel
from constants.database import DB_URL
import sentry_sdk


def main():
    """ Launching start here """

    sentry_sdk.init(
        dsn="https://6053c93c03077056f53f0034deed18fb@o4505942102638592.ingest.sentry.io/4505942105915392",
        traces_sample_rate=1.0,
    )

    db = DatabaseModel(DB_URL)
    epicevents = epicEvents()

    try:
        epicevents.login_menu()
    except KeyboardInterrupt as e:
        sentry_sdk.set_tag("application", "interrupt")
        sentry_sdk.capture_exception(e)
        print("\n\nFin du script par l'utilisateur.\n")
    finally:
        if db:
            print('Fermeture de la session MySql\n')
            db.get_session().close()

if __name__ == "__main__":
    main()
