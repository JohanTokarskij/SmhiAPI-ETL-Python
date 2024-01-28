import datetime
import os
import requests
from helper_functions import create_excel_headers, clear_or_create_sheet, wait_for_keypress
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import openpyxl
from time import sleep

EXCEL_FILE = 'Weather_dashboard.xlsx'
PRECIPITATION_CATEGORIES = {0: 'No precipitation',
                            1: 'Snow',
                            2: 'Snow and rain',
                            3: 'Rain',
                            4: 'Drizzle',
                            5: 'Freezing rain',
                            6: 'Freezing drizzle'}

# Extract data from SMHI Api #
def extract_smhi_data(latitude, longitude):
    """
    Fetches data from the SMHI API and extracts temperature and precipitation values for the next 24 hours for a given longitude and latitude.

    Returns:
        response.json()
    Raises:
        ValueError: If the latitude and longitude are outside the valid geographic area of SMHI.
        Exception: If an incorrect status code is returned from the API call.
    """

    try:
        response = requests.get(
            f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json')

        if response.status_code == 404:
            raise ValueError('The provided location are outside the valid geographic area of SMHI.')
        elif response.status_code != 200:
            raise Exception(f'Error fetching data: HTTP status code {response.status_code}')

        return response.json()

    except requests.RequestException as e:
        raise Exception(f'Error during API request: {e}')
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f'An unexpected error occurred: {e}')

# Transform data #
def transform_smhi_data(data, latitude, longitude,):
    """
    Transforms and returns fetched weather data into a structured format.

    Parameters:
    data (dict): A dictionary containing weather data from SMHI.

    Returns:
    List[List[Union[str, int, float]]]: A list of weather data where each sublist contains:
        0. 'fetched': Timestamp of when the data processing occurred ('YYYY-MM-DD hh:mm').
        1. 'longitude': Longitude of the observation location (in decimal degrees).
        2. 'latitude': Latitude of the observation location (in decimal degrees).
        3. 'date': Date of the weather data ('YYYY-MM-DD').
        4. 'hour': Hour of the day when data was observed (formatted as 'HH:00').
        5. 'temperature': Temperature at the time of observation (in °C).
        6. 'precipitation_category': Description of precipitation type (e.g., 'rain', 'snow').
        7. 'precipitation_mm': Amount of precipitation in mm.

    Raises:
    ValueError: If the input data is not in the expected format or missing required information.
    """
    
    try:
        transformed_data = []
        rounded_start_time = datetime.datetime.now() + datetime.timedelta(minutes=60 -
                                                                        datetime.datetime.now().minute)
        format_string = "%Y-%m-%d %H:%M"
        formatted_rounded_start_time = rounded_start_time.strftime(
            format_string)

        for _ in range(24):
            for observation in data['timeSeries']:
                if formatted_rounded_start_time == ' '.join(observation['validTime'].split('T'))[:-4]:
                    fetched = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    date = formatted_rounded_start_time.split(' ')[0]
                    hour = f'{int(formatted_rounded_start_time.split(
                        " ")[1].split(":")[0]):02d}:00'
                    temperature = [param['values'][0]
                                for param in observation['parameters'] if param['name'] == 't'][0]
                    precipitation_category_value = [
                        param['values'][0] for param in observation['parameters'] if param['name'] == 'pcat'][0]
                    precipitation_category = PRECIPITATION_CATEGORIES[precipitation_category_value]
                    precipitation_mm = [param['values'][0] for param in observation['parameters'] if param['name'] == 'pmedian'][0]
                    transformed_data.append([fetched, latitude, longitude, date,
                                            hour, temperature, precipitation_category, precipitation_mm])

                    rounded_start_time += datetime.timedelta(hours=1)
                    formatted_rounded_start_time = rounded_start_time.strftime(
                        format_string)
                    break
        return transformed_data
    
    except KeyError as ke:
        raise ValueError(f"Missing key in input data: {ke}")
    except TypeError as te:
        raise ValueError(f"Invalid data type in input: {te}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")

# Load data into Excel #
def load_data_to_excel(data, location):
    try:
        capitalized_location = location.capitalize()

        if os.path.exists(EXCEL_FILE):
            workbook = openpyxl.load_workbook(EXCEL_FILE)
        else:
            workbook = openpyxl.Workbook()
            print('\nExcel dashboard has been created.')
            sleep(0.75)
            workbook.remove(workbook['Sheet'])

        sheet = clear_or_create_sheet(workbook, capitalized_location)
        create_excel_headers(sheet)

        for value in data: 
            sheet.append(value)
        
        workbook.save(EXCEL_FILE)

    except FileNotFoundError:
        print(f"Error: The file {EXCEL_FILE} was not found.")
    except PermissionError:
        print(f"Error: Permission denied when accessing {EXCEL_FILE}.")
    except openpyxl.utils.exceptions.InvalidFileException:
        print(f"Error: The file {EXCEL_FILE} is not a valid Excel file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def etl(latitude, longitude, location):
    data = extract_smhi_data(latitude, longitude)
    transformed_data = transform_smhi_data(data, latitude, longitude)
    load_data_to_excel(transformed_data, location)

# MENU: 2. Update dashboard with the new data #
def update_dashboard(excel_file_path, etl_func):
    """
    Updates the dashboard with new data for each location listed in the Excel file.

    Args:
    excel_file_path (str): Path to the Excel file.
    etl_func (function): ETL function to execute for each location.
    """
    geolocator = Nominatim(user_agent='GeocodingApp')

    try:
        workbook = openpyxl.load_workbook(excel_file_path)
        sheet_names = workbook.sheetnames

        for location_name in sheet_names:
            try:
                location = geolocator.geocode(location_name)
                if location:
                    latitude, longitude = round(location.latitude, 6), round(location.longitude, 6)
                    etl_func(latitude, longitude, location_name)
                else:
                    print(f'Location not found for {location_name}.')
            except GeocoderTimedOut:
                print("Geocoder service timed out.")
            except GeocoderServiceError:
                print("Geocoder service error.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An error occurred while updating the dashboard: {e}")
        wait_for_keypress()


