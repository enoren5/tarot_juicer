import subprocess
import numpy
import pandas
import sys
from faker import Faker
from faker.providers import lorem
from pathlib import Path
from functools import partial


fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

LOREM = "Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split()


def bullets(num_bullets, words_per):
    return "\n".join(
        fake.sentence(nb_words=words_per, ext_word_list=LOREM, variable_nb_words=False)
        for _ in range(num_bullets)
    )


paragraph = partial(
    fake.paragraph, ext_word_list=LOREM, nb_sentences=6, variable_nb_sentences=True
)
word = partial(fake.word, ext_word_list=LOREM)
clear_screen = partial(subprocess.call, 'clear')
line = lambda width: print('=' * width)
"""
Prints fancy menu
"""
def menu(title, width = 80):
    line(width)
    print(f'{title:^{width}}')
    line(width)


"""
Simple function to iterate the current directory and return list of django apps
"""
def get_apps():
    cwd = Path('.')
    # simple lambda returns True if given dir is a django app, does it contain models.py
    is_app = lambda dir: len(list(dir.glob("models.py"))) > 0
    return [directory.name for directory in cwd.iterdir() if directory.is_dir() and is_app(directory)]


"""
Gets value for option from user input via prompt and loops until 'a' or valid option

Parameters:
    options : List
        list of valid options, first item is default
    prompt : prompt
        prompt text to use for input
"""
def get_option(options, prompt, title='MENU'):
    prompt += " ==> "
    choice =  len(options) + 1 # invalid choice gets loop started 
    valid_choices = [str(i) for i in range(1, len(options) + 1)]
    while choice not in valid_choices:
        clear_screen()
        # print menu
        menu(title)
        # show the options
        for i, option in enumerate(options):
            print(f'{i+1}: {option}')
        print(f'\nChoose one of {valid_choices}, 1 is default <enter>, "a" for abort\n')
        choice = input(prompt)
        if choice == 'a':
            sure = input('Are you sure? [y,n] ')
            if sure == 'y':
                sys.exit() # aborting
        elif choice == '':
            break;

    # value will be false if its empty, aka default first option 
    return options[int(choice) - 1] if choice else options[0]


"""
Gets options from the user with sane defaults
"""
def config():
    cfg = dict(database='internal', # (internal | external) internal => sqlite, external => heroku 
            app='essays', # app that we are targeting
            model='generators_generator' # target model for injection
            )
    target_db = get_option(['internal', 'external'], 'Which database should we use?')
    apps = get_apps()
    default = cfg['app']
    apps.remove(default) # remove default
    apps.insert(0, default) # insert default at first index
    app = get_option(apps, f'What is our target app? [{default}]')
    print(f'apps {apps}')
    print(f'default {default}')
    print(f'chose: {app}')
    print(f'chose: {target_db}')
    




if __name__ == "__main__":
    # get options
    config()
