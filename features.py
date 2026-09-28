import pandas as pd

df = pd.read_parquet('data/clean.parquet')

df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])
df['hour'] = df['scheduled_time'].dt.hour
df['dayofweek'] = df['scheduled_time'].dt.dayofweek
df['month'] = df['scheduled_time'].dt.month
df['is_weekend'] = df['dayofweek'].isin([5, 6])

feature_columns = ['hour', 'dayofweek', 'month', 'is_weekend', 'line', 'from', 'stop_sequence']

model_df = df[feature_columns + ['delayed', 'date']].copy()

model_df.to_parquet('data/features.parquet')

print(model_df.head())
print('\nRows:', len(model_df))
