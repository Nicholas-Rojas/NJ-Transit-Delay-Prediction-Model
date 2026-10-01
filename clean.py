import pandas as pd
import glob
import os

folder_path = './data/raw/*.csv'

all_files = glob.glob(folder_path)

excluded_files = ['invalid_trains_05-01-19_05-18-20.csv', 'invalid_trains.csv', '2020_03.csv', '2020_04.csv', '2020_05.csv']

## Collecting data and putting them into one dataFrame

def collect_data(files, ignore_files):
    
    df_list = []
    for file_path in files:

        file_name = os.path.basename(file_path)

        if file_name not in ignore_files:
            df = pd.read_csv(file_path)
            df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)

    return df


## Filtering data and saving to data/processed/

def filter_data(df):

    df = df[df["type"] == "NJ Transit"]

    df = df.dropna(subset=['scheduled_time', 'delay_minutes'])

    df["delayed"] = df["delay_minutes"] > 5

    

    return df



def main():

    ## Constructing our dataset

    df = collect_data(all_files, excluded_files)
    print(df.head())

    df = filter_data(df)

    ## Saving dataset
    df.to_parquet("data/processed/clean.parquet")

    ## Information to analyze dataset

    print('Rows after cleaning:', len(df))
    print('\nClass Balance:\n')
    print(df['delayed'].value_counts(normalize=True))


if __name__ == '__main__':

    main()