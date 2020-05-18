import time
from prompt_toolkit import PromptSession


session = PromptSession()

line = lambda width: print('=' * width)
clear_screen = partial(subprocess.call, 'clear')

def option_prompt(options, prompt='Choose one: ', show_menu=True,  title='[MENU]'):
    """
    Gets value for option from user input via prompt and loops until 'a' or valid option

    Parameters:
        options : List
            list of valid options, first item is default
        prompt : prompt
            prompt text to use for input
    """
    options.append('Abort!') 
    prompt += " ==> "
    choice =  len(options) + 1 # invalid choice gets loop started 
    valid_choices = [str(i) for i in range(1, len(options) + 1)]
    while choice not in valid_choices:
        menu(title, options)
        choice = session.prompt(prompt)
        # allow <enter> to be first choice *default
        if choice == '':
            return options[1]
            break
        # last choice "Abort!"
        elif type(choice) != int:
            print('Invalid choice...')
            time.sleep(2)
            choice = 99
            clear_screen()
            continue
        elif int(choice) == len(options):
            is_sure = session.prompt('Are you sure? [y,n] ==>')
            if is_sure == 'y':
                sys.exit() # aborting
            else:
                choice='x'

    # value will be false if its empty, aka default first option 
    return options[int(choice) - 1] if choice else options[0]

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

