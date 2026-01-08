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


# Calculates average temperature for each season

def seasonal_average(all_data):
    # Temperatures are grouped by season and averaged
    season_avg = all_data.groupby("Season")["Temperature"].mean()

    # Results are written to the required output file
    with open("average_temp.txt", "w", encoding="utf-8") as f:
        for season in SEASON_ORDER:
            f.write(f"{season}: {season_avg[season]:.1f}°C\n")


# Finds the station(s) with the largest temperature range

def largest_temperature_range(all_data):
    # Maximum and minimum temperatures are calculated per station
    station_stats = all_data.groupby("STATION_NAME")["Temperature"].agg(["max", "min"])

    # Temperature range is calculated as max minus min
    station_stats["range"] = station_stats["max"] - station_stats["min"]

    # The largest range value is identified
    largest_range_value = station_stats["range"].max()

    # All stations matching this range are selected
    largest_range_stations = station_stats[station_stats["range"] == largest_range_value]

    # Results are written to the output file
    with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
        for station, row in largest_range_stations.iterrows():
            f.write(
                f"{station}: Range {row['range']:.1f}°C "
                f"(Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n"
            )

# Finds the most stable and most variable stations

def temperature_stability(all_data):
    # Standard deviation is calculated for each station
    station_std = all_data.groupby("STATION_NAME")["Temperature"].std()

    # The smallest and largest standard deviation values are identified
    smallest_std = station_std.min()
    largest_std = station_std.max()

    most_stable_stations = station_std[station_std == smallest_std]
    most_variable_stations = station_std[station_std == largest_std]

    # Results are written to the output file
    with open("temperature_stability_stations.txt", "w", encoding="utf-8") as f:
        for station, std in most_stable_stations.items():
            f.write(f"Most Stable: {station}: StdDev {std:.1f}°C\n")

        for station, std in most_variable_stations.items():
            f.write(f"Most Variable: {station}: StdDev {std:.1f}°C\n")


# Main function that runs the full program

def main():
    all_data = load_all_years_data(TEMPERATURE_FOLDER)

    if all_data is None:
        return

    seasonal_average(all_data)
    largest_temperature_range(all_data)
    temperature_stability(all_data)

    print("Processing complete. Output files have been created.")


# Ensures the program runs only when this file is executed directly
if __name__ == "__main__":
    main()
