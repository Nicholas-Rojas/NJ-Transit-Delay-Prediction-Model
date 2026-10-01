import pandas as pd

weather_cols = ['datehour', 'temperature_2m', 'precipitation', 
                'snowfall', 'snow_depth', 'windgusts_10m']

base_features = ['hour', 'dayofweek', 'month', 'is_weekend', 'line', 
                 'from', 'stop_sequence', 'amtrak_count', 'prev_delay']

weather_features = ['temperature_2m', 'precipitation', 'snowfall', 'snow_depth',
                    'windgusts_10m', 'is_precip', 'is_snow', 'heavy_precip']



def add_time_features(df):

    df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])

    df['hour'] = df['scheduled_time'].dt.hour

    df['dayofweek'] = df['scheduled_time'].dt.dayofweek

    df['month'] = df['scheduled_time'].dt.month

    df['is_weekend'] = df['dayofweek'].isin([5, 6])

    df['datehour'] = df['scheduled_time'].dt.floor('h')

    return df


def add_prev_delay(df):

    df = df.sort_values(['train_id', 'date', 'stop_sequence'])

    df['prev_delay'] = df.groupby(['train_id', 'date'])['delay_minutes'].shift(1)

    return df


def add_amtrak(df, amtrak):

    df = df.merge(amtrak, on=['from', 'datehour'], how='left')

    df['amtrak_count'] = df['amtrak_count'].fillna(0)

    df = df.sort_values(['train_id', 'date', 'stop_sequence'])

    return df


def add_weather(df, weather):

    weather['datehour'] = pd.to_datetime(weather['time']).dt.floor('h')

    df = df.merge(weather[weather_cols], on='datehour', how='left')
    
    df['is_precip'] = df['precipitation'] > 0

    df['is_snow'] = df['snowfall'] > 0
    
    heavy_rain = df.loc[df['precipitation'] > 0, 'precipitation'].quantile(0.95)

    df['heavy_precip'] = df['precipitation'] > heavy_rain
    
    df['date'] = df['datehour'].dt.normalize()
    
    return df.drop(columns=['datehour'])


def main():

    df = pd.read_parquet('data/processed/clean.parquet')

    amtrak = pd.read_parquet('data/processed/amtrak_congestion.parquet')

    weather = pd.read_parquet('data/processed/weather.parquet')

    df = add_time_features(df)

    df = add_prev_delay(df)

    df = add_amtrak(df, amtrak)

    df = add_weather(df, weather)

    model_df = df[base_features + weather_features + ['delayed', 'date']].copy()


    print(model_df.head())
    print('\nRows:', len(model_df))
    print('Weather nulls:\n', model_df[['temperature_2m', 'precipitation']].isna().sum())
    print('heavy_precip share:', round(model_df['heavy_precip'].mean(), 4))

    model_df.to_parquet('data/processed/features.parquet')


if __name__ == '__main__':

    main()