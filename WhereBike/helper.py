import pandas as pd
from datetime import datetime

# Humidity: Mean = 0.627229
MEAN_HUM = 0.727229
# Windspeed: Mean = 0.190098
MEAN_WINDSPEED = 0.190098
# Weather: Mode = 1 (Clear)
MODE_WEATHER = 1

# Only used in vendor_generate_24h_features
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

a = {'temperature': '1', 'time': '23:47', 'weather': None, 'humidity': None, 'windspeed': None, 'date': '2023-12-05'}
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
    month = date_obj.month
    for i in range(2, 13):
        if month == i:
            result["mnth_" + str(i)] = 1
        else:
            result["mnth_" + str(i)] = 0
    # Year
    result["yr"] = date_obj.year

    # Working Day: Imputed with whether the day is a weekday
    if day < 5:
        result["workingday"] = 1
    else:
        result["workingday"] = 0

    # Holiday: Imputed with max_freq: 0
    result['holiday'] = 0

    # Humidity: Imputed with mean humidity
    result['hum'] = df['humidity']

    # Windspeed: Imputed with mean windspeed
    result["windspeed"] = df["windspeed"]
    
    # Weather: Imputed with mode weather      
    weather = df["weather"]    
    for i in range(2, 5):
        if i == weather:
            result["weathersit_" + str(i)] = 1
        else:
            result["weathersit_" + str(i)] = 0    
    return result

def vendor_generate_df(df):
    cnt_lag_1 = df["cnt_lag_1"]
    cnt_lag_2 = df["cnt_lag_2"]
    del df["cnt_lag_1"], df["cnt_lag_2"]
    result = user_generate_df(df)    
    # Attach lag variables to generated df
    result["cnt_lag_1"] = cnt_lag_1
    result["cnt_lag_2"] = cnt_lag_2
    return result

def vendor_generate_24h_df(df, model):
    start_hour = df['hr'].iloc[0]
    labels = [start_hour]
    values = [int(df["cnt"].iloc[0])]
    row = df
    for i in range(1, 6):
        new_hour = (start_hour + i) % 24  # This will loop the hour back to 0 after 23    
        labels.append(new_hour)            
        new_cnt_lag_1 = row["cnt"]
        new_cnt_lag_2 = row["cnt_lag_1"]
        row["hr"] = new_hour
        row["cnt_lag_1"] = new_cnt_lag_1
        row["cnt_lag_2"] = new_cnt_lag_2
        new_cnt = model.predict(row[features])
        new_cnt = round(new_cnt[0])
        values.append(new_cnt)
        row["cnt"] = new_cnt
    return labels, values
