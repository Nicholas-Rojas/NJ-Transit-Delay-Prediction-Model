import pandas as pd

df = pd.read_parquet('data/processed/clean.parquet')

df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['hour'] = df['scheduled_time'].dt.hour
df['dayofweek'] = df['scheduled_time'].dt.dayofweek
df['month'] = df['scheduled_time'].dt.month
df['is_weekend'] = df['dayofweek'].isin([5, 6])

df['datehour'] = df['scheduled_time'].dt.floor('h')

feature_columns = ['hour', 'dayofweek', 'month', 'is_weekend', 'line', 'from', 'stop_sequence']

model_df = df[feature_columns + ['delayed', 'datehour']].copy()

weather_df = pd.read_parquet('data/weather.parquet')
weather_df['datehour'] = pd.to_datetime(weather_df['time']).dt.floor('h')

weather_cols = ['datehour', 'temperature_2m', 'precipitation', 'snowfall', 'snow_depth', 'windgusts_10m']

def add_weather_features(df_weather, df_NJTransit):

    combined_df = df_NJTransit.merge(df_weather[weather_cols], on='datehour', how='left')

    combined_df['is_precip'] = combined_df['precipitation'] > 0
    combined_df['is_snow'] = combined_df['snowfall'] > 0

    heavy_rain = combined_df.loc[combined_df['precipitation'] > 0, 'precipitation'].quantile(0.95)
    combined_df['heavy_precip'] = combined_df['precipitation'] > heavy_rain

    combined_df['date'] = combined_df['datehour'].dt.normalize()

    return combined_df.drop(columns=['datehour'])


model_df = add_weather_features(weather_df, model_df)



print(model_df.head())
print('\nRows:', len(model_df))
print('Weather nulls:\n', model_df[['temperature_2m', 'precipitation']].isna().sum())
print('heavy_precip share:', round(model_df['heavy_precip'].mean(), 4))

model_df.to_parquet('data/processed/features.parquet')