import os
import glob
import pandas as pd

"""
This program analyses temperature data from multiple years.
Each CSV file represents one year of data.
The program reads all CSV files in the temperatures folder,
combines them, and performs the required calculations.
"""

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

# Order used when writing seasons to the output file
SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]



def find_season(month):
    """
    Converts a month name into its corresponding Australian season.

    Why this is a function:
    - The mapping logic is reused many times, so keeping it in one place
      makes the program easier to maintain and read.
    """
    try:
        for season, months in SEASONS.items():
            if month in months:
                return season
        return None
    except Exception as e:
        # If something weird happens, we return None so the program can keep going
        print(f"[Warning] find_season() had an issue: {e}")
        return None



# Reads all CSV files and combines them into one dataset

def load_all_years_data(folder_path):
    """
    Loads all CSV files from the folder and combines them into one DataFrame.

    What this function does (in simple steps):
    1) Finds every CSV file in the folder
    2) Reads each CSV using pandas
    3) Converts the 12 month columns into a long format using melt()
    4) Joins all years together so later calculations are easier
    """
    try:
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

        # Beginner-friendly check: if folder has no CSV files, stop early
        if len(csv_files) == 0:
            print("No CSV files found in the folder.")
            return None

        combined_data = []

        # Using a simple for loop so the process is clear
        for file_path in csv_files:
            try:
                df = pd.read_csv(file_path)

                # Melt makes the data easier to group by Month/Season later
                df_long = df.melt(
                    id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
                    value_vars=MONTHS,
                    var_name="Month",
                    value_name="Temperature"
                )

                combined_data.append(df_long)

            except Exception as e:
                # If one CSV file is broken, we skip it and continue with the rest
                print(f"[Warning] Skipping file due to error: {file_path}")
                print(f"          Reason: {e}")

        # If every file failed, combined_data will be empty
        if len(combined_data) == 0:
            print("All CSV files had issues. No data could be loaded.")
            return None

        all_data = pd.concat(combined_data, ignore_index=True)

        # Remove missing temperatures because they can mess up averages
        all_data = all_data.dropna(subset=["Temperature"])

        # Add season info once so other functions don’t repeat the logic
        all_data["Season"] = all_data["Month"].apply(find_season)

        return all_data

    except Exception as e:
        print(f"[Error] load_all_years_data() failed: {e}")
        return None

