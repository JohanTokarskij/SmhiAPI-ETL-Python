from etl_funcs import etl, update_dashboard, EXCEL_FILE
from helper_functions import get_coordinates, clear_screen, wait_for_keypress

def main_menu():
    while True:
        clear_screen(0)
        print('\n' + '*' * 40)
        print('MAIN MENU'.center(40))
        print('*' * 40)

        print('\n1. Add new location to Excel-dashboard')
        print('2. Update dashboard with the new data')
        print('3. Exit')

        choice = input('Enter your choice (1-3): ')

        if choice == '1':
            coordinates = get_coordinates()
            if coordinates:
                latitude, longitude, location = coordinates
                try:
                    etl(latitude, longitude, location)
                    print('\nData successfully added.')
                    clear_screen()
                except ValueError as ve:
                    print(f'\nError: {ve}')
                    wait_for_keypress()
                except Exception as e:
                    print(f'\nAn unexpected error occurred: {e}')
                    wait_for_keypress()
        elif choice == '2':
            try:
                update_dashboard(EXCEL_FILE, etl)
                print('\nDashboard updated successfully.')
                clear_screen()
            except Exception as e:
                print(f'\nAn error occurred while updating the dashboard: {e}')
                wait_for_keypress()
        elif choice == '3':
            print('\nExiting the application.')
            clear_screen()
            break
        else:
            print('\nInvalid choice. Please try again.')
            clear_screen()