import time
from prompt_toolkit import PromptSession
from functools import partial
from subprocess import call


session = PromptSession()

line = lambda width: print('=' * width)
clear_screen = partial(call, 'clear')

def option_prompt(options, prompt='Choose one:', show_menu=True,  title='[MENU]', cursor='==>'):
    """
    Gets value for option from user input via prompt and loops until 'a' or valid option

    Parameters:
        options : List
            list of valid options, first item is default
        prompt : prompt
            prompt text to use for input
    """
    options.append('Abort')
    if not show_menu:
        # short option
        valid_options = [option[0].lower() for option in options]
        options_fmt = ', '.join(f'[{option[0].lower()}]{option[1:]}' for option in options)
        prompt = f'{prompt} ({options_fmt}) {cursor} '
        while True:
            choice = session.prompt(prompt)
            if choice.isalpha() and choice in valid_options:
                break
        if choice == 'a':
            quit()
        else:
            choice = options[valid_options.index(choice)]
            return choice
    else:
        menu(title, options)
        valid_options = range(1, len(options) + 1)
        prompt = f'{prompt} {cursor} '
        while True:
            choice = session.prompt(prompt)
            if choice.isdigit() and int(choice) in valid_options:
                break
        choice = int(choice)
        if choice == len(options):
            quit()
        else:
            return choice

def menu(title, options, width = 80):
    """
    Prints fancy menu
    """
    print('\n')
    line(width)
    print(f'{title:^{width}}')
    line(width)

    # show the options
    for i, option in enumerate(options):
        print(f'{i+1}: {option}')
    print('\n')
