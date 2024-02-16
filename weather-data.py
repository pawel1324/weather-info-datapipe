import requests
import csv
import pandas as pd

#website of APIs https://open-meteo.com/
#API endpoint with weather data (example for historical data)
#URL = 'https://archive-api.open-meteo.com/v1/archive?latitude=52.2298&longitude=21.0118&start_date=2023-12-03&end_date=2023-12-03&hourly=temperature_2m,precipitation,wind_speed_10m'


#getting data for one city

start_date = input('Start date: ') 
end_date = input('End date: ')  

def get_weather_city(lat, lng, start_date, end_date):
    URL = f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lng}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,precipitation,wind_speed_10m'
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
        print(f"Błąd pobierania danych dla lat={lat}, lng={lng}: {response.status_code}")
        return None
#read about __main__
#getting data for all capitals of voivodeships
def get_weather_data():
    weather_data = []
    with open('weather-cities.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = row['lat']
            lng = row['lng']
            city = row['city']
            df = get_weather_city(lat, lng, start_date, end_date)
            if df is not None:
                df['city'] = city 
                weather_data.append(df)
                print(f'Pobrałem dane dla: {city}')
    return pd.concat(weather_data, ignore_index=True)

# export dataframe with weather data to .csv file
def weather_data_to_csv():
    weather_df = get_weather_data()
    weather_df.to_csv('weather_data.csv', index=False)
    
weather_data_to_csv()




