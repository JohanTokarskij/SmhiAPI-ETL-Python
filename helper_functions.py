import os
from geopy.geocoders import Nominatim


# Helper functions #
def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_keypress():
    while True:
        input('\nPress "Enter" to continue...')
        break

def create_excel_headers(sheet):
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    for column_letter in columns:
        sheet.column_dimensions[column_letter].width = 20

    sheet["A1"] = "Fetched"
    sheet["B1"] = "Latitude"
    sheet["C1"] = "Longitude"
    sheet["D1"] = "Date"
    sheet["E1"] = "Hour"
    sheet["F1"] = "Temperature"
    sheet["G1"] = "Precipitation Category"
    sheet["H1"] = "Precipitation in mm"

def get_coordinates():
    geolocator = Nominatim(user_agent="GeocodingApp")
    location = geolocator.geocode(input("Enter city name: "))

    latitude = None
    longitude = None

    if location:
        latitude = round(location.latitude, 6)
        longitude = round(location.longitude, 6)
        """ print(f'Coordinates for {location[0]} are: \n Latitude: {
              latitude}, Longitude: {longitude}\n') """
        #print(type(location[0].split(',')[0]))
        return latitude, longitude, location[0].split(',')[0]
    else:
        print('Geocoding failed. Check your input or try a different location.')
