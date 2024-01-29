from etl_funcs import etl, update_dashboard, EXCEL_FILE
from helper_functions import get_coordinates, clear_screen, wait_for_keypress
import questionary

def main_menu():
    while True:
        clear_screen(0)
        print('\n' + '*' * 40)
        print('MAIN MENU'.center(40))
        print('*' * 40 + '\n')

        choice = questionary.select(
            "Select an option:",
            choices=[
                "1. Add/Update Locations in Dashboard",
                "2. Update whole dashboard with the new data",
                "3. Exit"
            ]).ask()

        if choice == "1. Add/Update Locations in Dashboard":
            coordinates = get_coordinates()
            if coordinates:
                latitude, longitude, location = coordinates
                try:
                    etl(latitude, longitude, location)
                    wait_for_keypress()
                except ValueError as ve:
                    print(f'\nError: {ve}')
                    wait_for_keypress()
                except Exception as e:
                    print(f'\nAn unexpected error occurred: {e}')
                    wait_for_keypress()

        elif choice == "2. Update dashboard with the new data":
            try:
                update_dashboard(EXCEL_FILE, etl)
                wait_for_keypress()
            except Exception as e:
                print(f'\nAn error occurred while updating the dashboard: {e}')
                wait_for_keypress()

        elif choice == "3. Exit":
            print('\nExiting the application.')
            clear_screen()
            break

        elif choice is None:
            clear_screen()
            break
