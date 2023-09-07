from controllers.base import epicEvents

def main():
    """ launching starting here """
    epicevents = epicEvents()
    try:
        epicevents.main_menu()
    except KeyboardInterrupt:
        print("\n\nFin du script par l'utilisateur.\n")

if __name__ == "__main__":
    main()
