import os, time


def clear_screen():
    """ function to clear screan """
    
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system('cls')

def display_message(message, space_before, space_after,timing):
    """
    display message
    INPUT : message to display, True of False for space before and after message, timing for time to display message (pause=need [ENTER] to continue)
    OUTPUT : message displaying
    """

    if space_before:
        print()
    print(message)
    if space_after:
        print()
    if timing == 'pause':
        input()
    else:
        time.sleep(timing)

def input_message(message):
    """
    display input message
    INPUT : message to input
    OUTPUT : input message
    """

    answer = input(message)
    return answer
