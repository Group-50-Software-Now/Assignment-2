import os
import glob
import pandas as pd

# This program analyses temperature data from multiple years.
# Each CSV file represents one year of data.
# The program reads all CSV files in the temperatures folder,
# combines them, and performs the required calculations.


# Path to the folder that contains all the temperature CSV files
TEMPERATURE_FOLDER = r"C:\Users\rauni\OneDrive\Desktop\HIT137_Assignment2\temperatures"

# The dataset stores temperatures in these 12 month columns
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Australian seasons and the months that belong to each season
SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]



# Converts a month name into its corresponding season

def find_season(month):
    # Each month is checked against the season dictionary
    for season, months in SEASONS.items():
        if month in months:
            return season
    return None

# Reads all CSV files and combines them into one dataset
def load_all_years_data(folder_path):
    # All CSV files in the folder are collected
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if len(csv_files) == 0:
        print("No CSV files found in the folder.")
        return None

    combined_data = []

    # Each file is read and reshaped into a usable format
    for file_path in csv_files:
        df = pd.read_csv(file_path)
