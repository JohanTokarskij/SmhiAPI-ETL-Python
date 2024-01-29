import inquirer

questions = [
    inquirer.List('menu_option',
                  message="Select an option:",
                  choices=['Option 1', 'Option 2', 'Option 3']
                  )
]

answers = inquirer.prompt(questions)
print("You selected:", answers['menu_option'])
