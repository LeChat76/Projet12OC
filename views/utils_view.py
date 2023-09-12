import os, time


def clear_screen():
    """ function to clear screan """
    
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system('cls')

def display_message(message, spaces, timing):
    """
    display message
    INPUT : message to display, True of False for space before and after message, timing for time to display message
    OUTPUT : message displaying
    """

    if spaces:
        print()
    print(message)
    if spaces:
        print()
    time.sleep(timing)

def input_message(message):
    """
    display input message
    INPUT : message to input
    OUTPUT : input message
    """

    answer = input(message)
    return answer
