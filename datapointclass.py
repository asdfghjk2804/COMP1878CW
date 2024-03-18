#Task 1 - Class Creation
import requests
import pandas as pd
import os
import git

class DataPoint:
    """
    A class to interact with the Met Office Datapoint API.

    Attributes:
        api_key (str): The API key for accessing the Met Office Datapoint API.
    """

    def __init__(self, api_key):
        """
        Initializes the DataPoint object with the provided API key.

        Attributes:
            api_key (str): The API key for accessing the Met Office Datapoint API.
        """
        self.api_key = api_key

    def find_location_id(self, location_name):
        """
        Finds the ID of a location based on its name.

        Attributes:
            location_name (str): The name of the location to search for.

        Returns:
            str: The ID of the location if found.

        Raises:
            ValueError: If the location is not found in the API response.
        """
        begin_url = "http://datapoint.metoffice.gov.uk/public/data/"
        resource = "val/wxfcs/all/json/sitelist"
        url = f"{begin_url}{resource}?key={self.api_key}"

        try: 
            response = requests.get(url)
            data = response.json()
            print(data)  # Print the data to see its structure

            for location in data["Locations"]["Location"]:
                if location["name"] == location_name:
                    return location["id"]

            raise ValueError(f"The location '{location_name}' is not found.")
        
        except requests.exceptions.RequestException as x:
            print("Error in making the API request:", x)
            return None
        except ValueError as x:
            print("Error:", x)
            return None

    def get_forecast_data(self, location_ids):
        """
        Gets the weather forecast data for multiple locations.

        Attributes:
            Location_ids (list): A list of location ids.

        Returns:
            DataFrame: A DataFrame containing the weather forecast data.
        """
        begin_url = "http://datapoint.metoffice.gov.uk/public/data/"
        resource = "val/wxfcs/all/json/"
        forecast_days = 5
        forecast_hours = 8  

        every_forecasts = []
        for location_id in location_ids:
            url = f"{begin_url}{resource}{location_id}?res=3hourly&key={self.api_key}"

            try:
                response = requests.get(url)
                data = response.json()
                print(data)  # Print the data to see its structure

                periods = data["SiteRep"]["DV"]["Location"]["Period"]  # Access the Period array directly

                for period in periods:
                  forecasts = period.get("Rep", [])  # Use .get() to handle missing "Rep" key gracefully
                  for forecast in forecasts:
                    forecast["Location_ID"] = location_id
                    every_forecasts.append(forecast)
                
            
            except requests.exceptions.RequestException as x:
                print("Error in making the API request:", x)
                return None
        
        # Convert to DataFrame
        df = pd.DataFrame(every_forecasts)
        return df

#Task 2 - Data Handling

    def save_raw_data(self, df, forecast_data):
        """
        Saves the raw forecast data to a CSV file.

        Attributes:
            df : The DataFrame containing the raw forecast data.
            forecast_data (str): The name of the CSV file.
        """
        #df.to_csv(f"data/{forecast_data}.csv", index=False)
        # Get the root directory of the Git repository
        repo = git.Repo(search_parent_directories=True)
        git_repository_path = repo.git.rev_parse("--show-toplevel")
        
        # Create a 'data' directory in the Git repository if it doesn't exist
        data_directory = os.path.join(git_repository_path, "data")
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        
        # Save the CSV file to the 'data' directory in the Git repository
        csv_path = os.path.join(data_directory, f"{forecast_data}.csv")
        df.to_csv(csv_path, index=False)

    def replace_headings(self, df, headings_dict):
        """
        Replaces the headings in the DataFrame with the provided dictionary mapping.

        Attributes:
            df : The DataFrame where the headings need to be replaced.
            headings_dict (dict): A dictionary mapping of the old headings to new headings.
        """
        df.rename(columns=headings_dict, inplace=True)

    def remove_ext_column(self, df, column_name):
        """
        Removes an extra column from the DataFrame.

        Attributes:
            df : The DataFrame from which the extra column needs to be removed.
            column_name (str): The name of the column to remove.
        """
        if column_name in df.columns:
            df.drop(columns=[column_name], inplace=True)

    def group_similar_weather(self, df, weather_mapping):
        """
        Groups similar types of weather in the DataFrame according to the provided mapping.

        Attributes:
            df : The DataFrame containing the weather data.
            weather_mapping : A dictionary mapping weather codes to similar descriptions.
        """
        df["Weather Type"] = df["Weather Type"].map(weather_mapping)


api_key = "3ee03133-29bb-4cef-b5c1-4ad422daf97c"
data = DataPoint(api_key)
location_ids = ["99005", "324172"] #replace w real locations, random locations done
forecast_data = data.get_forecast_data(location_ids)

# save raw data to a csv file
data.save_raw_data(forecast_data, "forecast_data")

# define mapping for headings and grouping similar weather
headings_dict = {'D': 'Wind Direction', 'F': 'Feels Like Temperature', 'G': 'Wind Gust',
                 'H': 'Screen Relative Humidity', 'Pp': 'Precipitation Probability',
                 'S': 'Wind Speed', 'T': 'Temperature', 'V': 'Visibility',
                 'W': 'Weather Type', 'U': 'Max UV Index'}

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

#replacing and cleaning the data
data.replace_headings(forecast_data, headings_dict)
data.remove_ext_column(forecast_data, "$")
data.group_similar_weather(forecast_data, weather_mapping)
