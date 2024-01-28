import datetime
import os
import requests
from helper_functions import create_excel_headers
import openpyxl

EXCEL_FILE = 'Weather_data.xlsx'
latitude = 59.3099
longitude = 18.0215



PRECIPITATION_CATEGORIES = {0: 'No precipitation',
                            1: 'Snow',
                            2: 'Snow and rain',
                            3: 'Rain',
                            4: 'Drizzle',
                            5: 'Freezing rain',
                            6: 'Freezing drizzle'}

# Extract data from SMHI Api #
def extract_smhi_data(latitude, longitude, location):
    """
    Fetches data from the SMHI API and extracts temperature and precipitation values for the next 24 hours for a given longitude and latitude.

    Returns:
        response.json()
    Raises:
        Exception: If an incorrect status code is returned from the API call.
    """

    try:
        response = requests.get(
            f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json')

        if response.status_code != 200:
            raise Exception(f'Error fetching data: HTTP status code {
                            response.status_code}')

        data = response.json()
        return data, location

    except requests.RequestException as e:
        raise Exception(f'Error during API request: {e}')

    except Exception as e:
        raise Exception(f'An error occurred: {e}')

# Transform data #
def transport_smhi_data(data, location):
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
        print(transformed_data)
        return transformed_data, location
    except KeyError as ke:
        raise ValueError(f"Missing key in input data: {ke}")
    except TypeError as te:
        raise ValueError(f"Invalid data type in input: {te}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")

# Load data into Excel #
def load_excel_data(data, location):
    capitalized_location = location.capitalize()
    if os.path.exists(EXCEL_FILE):
        workbook = openpyxl.load_workbook(EXCEL_FILE)

        if capitalized_location in workbook.sheetnames:
            sheet = workbook[capitalized_location]
        else:
            sheet = workbook.create_sheet(title=capitalized_location)
            create_excel_headers(sheet)

    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = capitalized_location
        create_excel_headers(sheet)

    for value in data: 
        sheet.append(value)
    
    workbook.save(EXCEL_FILE)



#get_coordinates()

