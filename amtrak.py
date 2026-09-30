import pandas as pd
import glob

files = [f for f in sorted(glob.glob('data/raw/*.csv')) if 'invalid' not in f]

frames = []

for f in files:
    d = pd.read_csv(f, usecols=['from', 'actual_time', 'type'])
    frames.append(d[d['type'] == 'Amtrak'])


amtrak = pd.concat(frames, ignore_index=True)
amtrak['actual_time'] = pd.to_datetime(amtrak['actual_time'])
amtrak['datehour'] = amtrak['actual_time'].dt.floor('h')

congestion = (amtrak.groupby(['from', 'datehour'])
                    .size()
                    .reset_index(name='amtrak_count'))

congestion.to_parquet('data/processed/amtrak_congestion.parquet', index=False)

print("congestion table shape:", congestion.shape)
print(congestion['amtrak_count'].describe())
print("\nbusiest station-hours:")
print(congestion.sort_values('amtrak_count', ascending=False).head())