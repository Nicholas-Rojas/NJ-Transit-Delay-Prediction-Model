import pandas as pd
import glob

folder_path = 'data/raw/*.csv'
all_files = glob.glob(folder_path)

## Extract only amtrak trains

def extract_amtrak():

    files = [f for f in sorted(all_files) if 'invalid' not in f]

    frames = []

    for file in files:
        df = pd.read_csv(file, usecols=['from', 'actual_time', 'type'])
        frames.append(df[df['type'] == 'Amtrak'])


    amtrak = pd.concat(frames, ignore_index=True)

    return amtrak

## Change actual time to datetime type and adding datehour

def edify_amtrak(df):

    df['actual_time'] = pd.to_datetime(df['actual_time'])
    df['datehour'] = df['actual_time'].dt.floor('h')

    amtrak_congestion = (df.groupby(['from', 'datehour'])
                        .size()
                        .reset_index(name='amtrak_count'))

    return amtrak_congestion


def main():

    ## Testing / Analyzing

    df = extract_amtrak()

    print(df.head())

    congestion = edify_amtrak(df)

    ## Saves Amtrak

    congestion.to_parquet('data/processed/amtrak_congestion.parquet', index=False)

    print("congestion table shape:", congestion.shape)
    print(congestion['amtrak_count'].describe())
    print("\nbusiest station-hours:")
    print(congestion.sort_values('amtrak_count', ascending=False).head())

if __name__ == '__main__':

    main()