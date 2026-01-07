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

 # Monthly temperature columns are converted into
        # one column called 'Temperature' with a matching 'Month'
        df_long = df.melt(
            id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
            value_vars=MONTHS,
            var_name="Month",
            value_name="Temperature"
        )

        combined_data.append(df_long)

    # All yearly datasets are merged into a single table
    all_data = pd.concat(combined_data, ignore_index=True)

    # Rows with missing temperature values are removed
    all_data = all_data.dropna(subset=["Temperature"])

    # A new column is added to identify the season for each month
    all_data["Season"] = all_data["Month"].apply(find_season)

    return all_data
