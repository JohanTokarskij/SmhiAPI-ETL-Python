from etl_funcs import extract_smhi_data, transport_smhi_data, load_excel_data
from helper_functions import get_coordinates

latitude = 59.3099
longitude = 18.0215

if __name__ == '__main__':
    while True:
        latitude, longitude, location = get_coordinates()
        data, location = extract_smhi_data(latitude, longitude, location)
        transformed_data, location = transport_smhi_data(data, location)
        load_excel_data(transformed_data, location)
        print('Done')
