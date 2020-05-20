import time
import click
from prompt_toolkit import PromptSession
from functools import partial
from subprocess import call


session = PromptSession()

clear_screen = partial(call, 'clear')

def multiple_choice(prompt, options, title='[CHOOSE ONE]',  default=None):
    choices = click.Choice(str(i) for i in range(1, len(options) +1))
    if default:
        default_choice = str(options.index(default))
    else:
        default_choice = '1'
    menu(title, options)
    choice = click.prompt(prompt,
            default=default_choice,
            type=choices,
            prompt_suffix=': ',
            show_choices=False)
    # minus 1 for zero based
    return options[int(choice) - 1]




line = lambda width=80, char='=': f'{char}' * width
heading = lambda title, width=80: f'{title:^{width}}'

def menu(title, options, width = 80):
    """
    Prints fancy menu
    """
    print(line())
    print(heading(title,width))
    print(line())

    # show the options
    for i, option in enumerate(options):
        print(f'{i+1}: {option}')
    print('\n')
