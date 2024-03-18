from datapointclass.py import DataPoint
import pandas as pd

# Read API key from a separate file
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()

# Instantiate the DataPoint class
data = DataPoint(api_key)

# Get location IDs
location_ids = [data.find_location_id("London"), data.find_location_id("Manchester")]

# Get forecast data
forecast_data = data.get_forecast_data(location_ids)

# Save raw data to CSV
forecast_data.to_csv("data/raw_data.csv", index=False)

# Replace headings with human-readable versions
human_readable_headings = {
    'D': 'Wind Direction',
    'F': 'Feels Like Temperature',
    'G': 'Wind Gust',
    'H': 'Screen Relative Humidity',
    'Pp': 'Precipitation Probability',
    'S': 'Wind Speed',
    'T': 'Temperature',
    'V': 'Visibility',
    'W': 'Weather Type',
    'U': 'Max UV Index'
}

forecast_data = forecast_data.rename(columns=human_readable_headings)

# Remove the extra column with the '$' heading
forecast_data = forecast_data.drop(columns=['$'], errors='ignore')

# Weather type mapping
weather_dict = {"NA": "Not available",
        "-1": "Trace rain",
        "0": "Clear night",
        "1": "Sunny day",
        "2": "Partly cloudy (night)",
        "3": "Partly cloudy (day)",
        "4": "Not used",
        "5": "Mist",
        "6": "Fog",
        "7": "Cloudy",
        "8": "Overcast",
        "9": "Light rain shower (night)",
        "10": "Light rain shower (day)",
        "11": "Drizzle",
        "12": "Light rain",
        "13": "Heavy rain shower (night)",
        "14": "Heavy rain shower (day)",
        "15": "Heavy rain",
        "16": "Sleet shower (night)",
        "17": "Sleet shower (day)",
        "18": "Sleet",
        "19": "Hail shower (night)",
        "20": "Hail shower (day)",
        "21": "Hail",
        "22": "Light snow shower (night)",
        "23": "Light snow shower (day)",
        "24": "Light snow",
        "25": "Heavy snow shower (night)",
        "26": "Heavy snow shower (day)",
        "27": "Heavy snow",
        "28": "Thunder shower (night)",
        "29": "Thunder shower (day)",
        "30": "Thunder"}
weather_mapping = {"NA": "Not available",
        "-1": "Trace rain",
        "0": "Clear",
        "1": "Clear",
        "2": "Partly cloudy",
        "3": "Partly cloudy",
        "4": "Not used",
        "5": "Low visibility",
        "6": "Low visibility",
        "7": "Cloudy",
        "8": "Cloudy",
        "9": "Light rain",
        "10": "Light rain",
        "11": "Light rain",
        "12": "Light rain",
        "13": "Heavy rain",
        "14": "Heavy rain",
        "15": "Heavy rain",
        "16": "Sleet",
        "17": "Sleet",
        "18": "Sleet",
        "19": "Hail",
        "20": "Hail",
        "21": "Hail",
        "22": "Light snow",
        "23": "Light snow",
        "24": "Light snow",
        "25": "Heavy snow",
        "26": "Heavy snow",
        "27": "Heavy snow",
        "28": "Thunder",
        "29": "Thunder",
        "30": "Thunder"}

forecast_data['Weather Type'] = forecast_data['Weather Type'].map(weather_mapping)

# Save processed data to CSV
forecast_data.to_csv("data/data_processed.csv", index=False)
