# Weather Dashboard Generator

This project is a Python-based application that fetches weather data for specified locations and creates an Excel dashboard with a 24-hour forecast. It utilizes the SMHI API to extract weather information and `openpyxl` to manage Excel file operations.

## Project Description

The application provides a menu-driven interface allowing users to:

1. **Add New Location to Excel-Dashboard**: Fetches weather data for a new location and saves it to the Excel dashboard "Weather_dashboard.xlsx" in the root directory of the project.
2. **Update Dashboard with New Data**: Updates the existing dashboard with the latest weather data for all listed locations.
3. **Exit**: Exits the application.

The result is an Excel dashboard that visually presents the weather forecast data, including temperature, precipitation, and other relevant details.

## Installation

This project was developed and tested using Python 3.12. To set up and run this project, follow these steps:

1. Clone the repository: `git clone [repository URL]`
2. Navigate to the project directory: `cd [project directory]`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage

Run the application by executing the app.py script:

`python app.py`

Follow the on-screen prompts to add locations, update the dashboard, or exit the application.

## Note: 
This project serves as a demonstration of ETL (Extract, Transform, Load) processes and Python scripting, and was developed for educational purposes. It showcases how to fetch, process, and load weather forecast data into an Excel dashboard.

## Area Limitation for SMHI API:
The application uses the SMHI API for weather data retrieval. It's important to note that the SMHI API has geographical limitations. For Point requests, the API accepts any longitude and latitude within its valid geographic area. If a user requests a point outside this area, the application will display the error message: "The provided location is outside the valid geographic area of SMHI." However, the API works perfectly for all Scandinavian countries and other nearby regions.