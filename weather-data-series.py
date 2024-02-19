import requests
import csv
import pandas as pd
from datetime import datetime, timedelta
import os

#website of APIs https://open-meteo.com/
#API endpoint with weather data (example for historical data)
#URL = 'https://archive-api.open-meteo.com/v1/archive?latitude=52.2298&longitude=21.0118&start_date=2023-12-03&end_date=2023-12-03&hourly=temperature_2m,precipitation,wind_speed_10m'


#function based on the start and end dates, creates lists with dates for iteration
def get_dates_list(start_date, end_date):
    dates_list = []
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    current_date = start_date
    while current_date <= end_date:
        dates_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return dates_list

start_date = input('Start date: ')
end_date = input('End date: ')

#downloading data for one city and for one day
def get_weather_city(lat, lng, date):
    URL = f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lng}&start_date={date}&end_date={date}&hourly=temperature_2m,precipitation,wind_speed_10m'
    response = requests.get(URL)
    if response.status_code == 200:
        json_data = response.json()
        df = pd.DataFrame({
            'time': json_data['hourly']['time'],
            'temperature': json_data['hourly']['temperature_2m'],
            'precipitation': json_data['hourly']['precipitation'],
            'wind': json_data['hourly']['wind_speed_10m'],
            'latitude': json_data['latitude'],
            'longitude': json_data['longitude']
            })
        return df
    else:
        print(f"Error downloading data for: {lat}, lng={lng}: {response.status_code}")
        return None

#downloading data for all voivodeship capitals for one day
def get_weather_data(date):
    weather_data = []
    with open('weather-cities.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = row['lat']
            lng = row['lng']
            city = row['city']
            df = get_weather_city(lat, lng, date)
            if df is not None:
                df['city'] = city 
                weather_data.append(df)
                print(f'Downloading data for: {city}')
            
    return pd.concat(weather_data, ignore_index=True)

#create folder for raw data and downloading weather data for all cities and dates
def get_data_all_dates():
    folder_name = 'weather_raw_data' 
    os.makedirs(folder_name, exist_ok=True)  
    
    for date in get_dates_list(start_date, end_date):
        weather_df = get_weather_data(date)  
        file_path = os.path.join(folder_name, f'weather_data_{str(date)}.csv')  
        weather_df.to_csv(file_path, index=False)

get_data_all_dates()





