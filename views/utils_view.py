import os, time


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system('cls')

def display_message(message, espaces, timing):
    """ display message """

    if espaces:
        print()
    print(message)
    if espaces:
        print()
    time.sleep(timing)

def input_message(message):
    """ display input message """

    answer = input(message)
    return answer
