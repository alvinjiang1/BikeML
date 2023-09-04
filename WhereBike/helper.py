import pandas as pd
from datetime import datetime

# Humidity: Mean = 0.627229
# Windspeed: Mean = 0.190098
# Weather: Mode = 1 (Clear)


features = ['yr',
 'hr',
 'holiday',
 'workingday',
 'temp',
 'hum',
 'windspeed',
 'weathersit_2',
 'weathersit_3',
 'weathersit_4',
 'mnth_2',
 'mnth_3',
 'mnth_4',
 'mnth_5',
 'mnth_6',
 'mnth_7',
 'mnth_8',
 'mnth_9',
 'mnth_10',
 'mnth_11',
 'mnth_12',
 'weekday_1',
 'weekday_2',
 'weekday_3',
 'weekday_4',
 'weekday_5',
 'weekday_6',
 'cnt_lag_1',
 'cnt_lag_2']

no_lag_features = ['yr',
 'hr',
 'holiday',
 'workingday',
 'temp',
 'hum',
 'windspeed',
 'weathersit_2',
 'weathersit_3',
 'weathersit_4',
 'mnth_2',
 'mnth_3',
 'mnth_4',
 'mnth_5',
 'mnth_6',
 'mnth_7',
 'mnth_8',
 'mnth_9',
 'mnth_10',
 'mnth_11',
 'mnth_12',
 'weekday_1',
 'weekday_2',
 'weekday_3',
 'weekday_4',
 'weekday_5',
 'weekday_6']

a = {'temperature': '1', 'time': '23:47', 'weather': 'weather2', 'humidity': '2', 'windspeed': '0', 'date': '2023-09-05'}
def user_generate_df(df):
    result = pd.DataFrame(index = [0], columns = no_lag_features)
    
    # Temperature
    result['temp'][0] = df['temperature']

    # Time
    result['hr'][0] = df['time']

    # Date    
    date_obj = datetime.strptime(df["date"], '%Y-%m-%d')
    day = date_obj.weekday()
    for i in range(6):
        if day == i:
            result['weekday_' + str(i + 1)] = 1
        else:
            result['weekday_' + str(i + 1)] = 0
    # Month

    # Year

    # Working Day

    # Holiday

    # Humidity

    # Windspeed
user_generate_df(a)