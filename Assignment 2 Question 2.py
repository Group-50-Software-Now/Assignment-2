import os
import glob
import pandas as pd

# Program Overview

"""
This program analyses historical temperature data collected over
multiple years from CSV files.

Each CSV file represents one year of temperature data recorded at
different weather stations. The program combines all files into a
single dataset and performs three main analyses:
1. Seasonal average temperatures (Australian seasons)
2. Stations with the largest temperature range
3. Most stable and most variable temperature stations

The results are written to separate output text files as required
by the assignment specification.
"""

# Path to the folder that contains all the temperature CSV files
TEMPERATURE_FOLDER = r"C:\Users\rauni\OneDrive\Desktop\HIT137_Assignment2\temperatures"

# List of month columns present in the dataset
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Australian seasons mapped to their corresponding months
SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}
# Order used to display seasonal results consistently
SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]


# Function: find_season

def find_season(month):
    """
    Determines which Australian season a given month belongs to.

    This function exists to convert month-based temperature data
    into season-based data, which is required for calculating
    seasonal averages.

    Parameters:
        month (str): Name of the month (e.g., "January")

    Returns:
        str: The corresponding season name, or None if not found
    """
    for season, months in SEASONS.items():
        if month in months:
            return season
    return None

# Function: load_all_years_data
def load_all_years_data(folder_path):
      """
    Reads all yearly CSV files and combines them into a single dataset.

    This function is necessary because the data is spread across
    multiple files (one per year). It reshapes the monthly columns
    into a long format so that temperature values can be analysed
    consistently across months, seasons, and stations.

    Parameters:
        folder_path (str): Path to the directory containing CSV files

    Returns:
        pandas.DataFrame: A cleaned and combined dataset containing
                          station details, month, season, and temperature
    """
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if len(csv_files) == 0:
        print("No CSV files found in the folder.")
        return None

    combined_data = []

    # Each file is read and reshaped into a usable format
    for file_path in csv_files:
        df = pd.read_csv(file_path)

   # Convert wide monthly data into a long, analysis-friendly format
        df_long = df.melt(
            id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
            value_vars=MONTHS,
            var_name="Month",
            value_name="Temperature"
        )

        combined_data.append(df_long)

     # Merge all years into one dataset
    all_data = pd.concat(combined_data, ignore_index=True)

     # Remove rows with missing temperature values
    all_data = all_data.dropna(subset=["Temperature"])

   # Assign a season to each month for seasonal analysis
    all_data["Season"] = all_data["Month"].apply(find_season)

    return all_data


# Function: seasonal_average

def seasonal_average(all_data):
    """
    Calculates the average temperature for each Australian season.

    This function supports high-level climate analysis by summarising
    temperature patterns across seasons rather than individual months.
    The results are written to a text file in a clear, readable format.

    Parameters:
        all_data (pandas.DataFrame): Combined temperature dataset
    """
    season_avg = all_data.groupby("Season")["Temperature"].mean()

    # Results are written to the required output file
    with open("average_temp.txt", "w", encoding="utf-8") as f:
        for season in SEASON_ORDER:
            f.write(f"{season}: {season_avg[season]:.1f}°C\n")


# Function: largest_temperature_range

def largest_temperature_range(all_data):
     """
    Identifies the weather station(s) with the largest temperature range.

    The temperature range (maximum minus minimum) helps highlight
    stations that experience the most extreme climate variations.
    This is useful for understanding regional climate behaviour.

    Parameters:
        all_data (pandas.DataFrame): Combined temperature dataset
    """
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

# Function: temperature_stability

def temperature_stability(all_data):
    """
    Determines the most stable and most variable temperature stations.

    Standard deviation is used as a measure of stability. A lower
    standard deviation indicates consistent temperatures, while a
    higher value indicates greater fluctuation over time.

    Parameters:
        all_data (pandas.DataFrame): Combined temperature dataset
    """
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


# Function: main
def main():
     """
    Acts as the entry point for the program.

    This function coordinates the overall workflow by:
    - Loading and cleaning the data
    - Running all required analyses
    - Producing the final output files

    Keeping this logic in one place improves readability and
    makes the program easier to maintain and test.
    """
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
