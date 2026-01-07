import os
import glob
import pandas as pd

# ------------------------------------------------------------
# This program analyses temperature data from multiple years.
# Each CSV file represents one year of data.
# The program reads all CSV files in the temperatures folder,
# combines them, and performs the required calculations.
# ------------------------------------------------------------

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

