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

 # Calculates average temperature for each season

# -----------------------------------------------------------
 def seasonal_average(all_data):
 """
 Calculates the average temperature for each season and saves it to a file.
 
 Using a loop for output writing makes the output order consistent
 (Summer, Autumn, Winter, Spring) every time.
 """
 try:
 season_avg = all_data.groupby("Season")["Temperature"].mean()
 
 with open("average_temp.txt", "w", encoding="utf-8") as f:
 # Using a while loop here just to show you can do it both ways (beginner style)
 i = 0
 while i < len(SEASON_ORDER):
 season = SEASON_ORDER[i]
 
 # Sometimes a season might be missing from data, so we handle it safely
 if season in season_avg.index:
 f.write(f"{season}: {season_avg[season]:.1f}°C\n")
 else:
 f.write(f"{season}: No data\n")
 
 i += 1
 
 except Exception as e:
 print(f"[Error] seasonal_average() failed: {e}")
 
 

 # Finds the station(s) with the largest temperature range

 def largest_temperature_range(all_data):
 """
 Finds the station(s) with the largest temperature range (max - min)
 and writes the result to a file.
 
 Range is useful because it shows which station experiences the biggest
 temperature swings in the dataset.
 """
 try:
 station_stats = all_data.groupby("STATION_NAME")["Temperature"].agg(["max", "min"])
 station_stats["range"] = station_stats["max"] - station_stats["min"]
 
 largest_range_value = station_stats["range"].max()
 largest_range_stations = station_stats[station_stats["range"] == largest_range_value]
 
 with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
 # for loop is clean and readable for writing multiple results
 for station, row in largest_range_stations.iterrows():
 f.write(
 f"{station}: Range {row['range']:.1f}°C "
 f"(Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n"
 )
 
 except Exception as e:
 print(f"[Error] largest_temperature_range() failed: {e}")
 
 
 
 # Finds the most stable and most variable stations

 def temperature_stability(all_data):
 """
 Finds the most stable and most variable stations using standard deviation.
 
 Beginner explanation:
 - Standard deviation shows how much values spread out.
 - Small std dev = temperatures are more consistent (stable).
 - Large std dev = temperatures change a lot (variable).
 """
 try:
 station_std = all_data.groupby("STATION_NAME")["Temperature"].std()
 
 # Picking min and max gives us the most stable and most variable stations
 smallest_std = station_std.min()
 largest_std = station_std.max()
 
 most_stable_stations = station_std[station_std == smallest_std]
 most_variable_stations = station_std[station_std == largest_std]
 
 with open("temperature_stability_stations.txt", "w", encoding="utf-8") as f:
 for station, std in most_stable_stations.items():
 f.write(f"Most Stable: {station}: StdDev {std:.1f}°C\n")
 
 for station, std in most_variable_stations.items():
 f.write(f"Most Variable: {station}: StdDev {std:.1f}°C\n")
 
 except Exception as e:
 print(f"[Error] temperature_stability() failed: {e}")
 
 # Main function that runs the full program

 def main():
 """
 Runs the full temperature analysis program.
 
 The try/except here is like a safety net:
 if something unexpected happens, we show the error message
 instead of crashing with a long traceback.
 """
 try:
 all_data = load_all_years_data(TEMPERATURE_FOLDER)
 
 # If loading failed, we stop politely
 if all_data is None:
 return
 
 seasonal_average(all_data)
 largest_temperature_range(all_data)
 temperature_stability(all_data)
 
 print("Processing complete. Output files have been created.")
 
 except Exception as e:
 print(f"[Error] main() failed: {e}")
 
 
 # Ensures the program runs only when this file is executed directly
 if __name__ == "__main__":
 main()
     
