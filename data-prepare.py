import pandas as pd

#download .csv file with polish cities from https://simplemaps.com/data/pl-cities

# preparation of data with voivodeship cities in .csv format
df = pd.read_csv('cities.csv', sep = ',', encoding = 'utf-8')
capitals = df[(df['capital'] == 'admin') | (df['capital'] == 'primary')]
capitals.loc[capitals['city'] == 'Warsaw', 'city'] = 'Warszawa'
capitals = capitals[['city', 'admin_name', 'country', 'population', 'lat', 'lng']]
capitals.to_csv('weather-cities.csv', index=False, header=True)

# slow changing dimension (SCD) read about it 