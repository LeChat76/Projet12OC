from controllers.base import epicEvents
from models.database_model import DatabaseModel
from constants.database import DB_URL_GUEST
from constants.sentry import DSN
from utils.utils_sentry import send_to_sentry_NOK
from utils.utils_view import display_message
import sentry_sdk, sys


def main():
    """ Launching start here """

    sentry_sdk.init(
        dsn=DSN,
        traces_sample_rate=1.0,
    )
    while True:
        try:
            db = DatabaseModel(DB_URL_GUEST)
            epicevents = epicEvents()
        except Exception as e:
            send_to_sentry_NOK("databose", "open", e)
            display_message(
                "Probleme lors de l'ouverture de la base de donnée." +
                "\nVoir logs Sentry pour plus de détails.",
                True,
                True,
                0
            )
            break

        try:
            epicevents.login_menu(autologin)
        except KeyboardInterrupt as e:
            send_to_sentry_NOK("application", "interrupt", e)
            display_message("\nFin du script par l'utilisateur.\n", True, False, 0)
            break
        finally:
            if db:
                display_message("Fermeture de la session MySql.", False, True, 0)
                db.get_session().close()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--token":
        autologin = True
        main()
    else:
        autologin = False
        main()

