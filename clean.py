import pandas as pd
import glob
import os

folder_path = './data/*.csv'
all_files = glob.glob(folder_path)

excluded_files = ['invalid_trains_05-01-19_05-18-20.csv', 'invalid_trains.csv', '2020_03.csv', '2020_04.csv', '2020_05.csv']

df_list = []

for file_path in all_files:

    file_name = os.path.basename(file_path)

    if file_name not in excluded_files:
        df = pd.read_csv(file_path)
        df_list.append(df)



df = pd.concat(df_list, ignore_index=True)
#print(df.head())   


df = df[df["type"] == "NJ Transit"]
df = df.dropna(subset=['scheduled_time', 'delay_minutes'])

df["delayed"] = df["delay_minutes"] > 5

df.to_parquet("data/clean.parquet")


print('Rows after cleaning:', len(df))
print('\nClass Balance:\n')
print(df['delayed'].value_counts(normalize=True))

print()
print()

daFa = pd.read_parquet("data/clean.parquet")
print(daFa.columns.tolist())
print(daFa[["scheduled_time"]].head())