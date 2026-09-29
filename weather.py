import time
import requests
import pandas as pd

# Location set at Newark for all trains/stops
LATITUDE = 40.7357
LONGITUDE = -74.1724

START_DATE = "2018-03-01"
END_DATE = "2020-02-29"

HOURLY_VARS = [
    "temperature_2m",
    "precipitation",
    "rain",
    "snowfall",
    "snow_depth",
    "windspeed_10m",
    "windgusts_10m",
    "weathercode",
]

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
OUTPUT_PATH = "data/weather.parquet"
 
 
def fetch_weather(lat, lon, start, end, hourly_vars, retries=3):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": ",".join(hourly_vars),
        "timezone": "America/New_York",
    }
    for attempt in range(1, retries + 1):
        resp = requests.get(ARCHIVE_URL, params=params, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        print(f"  attempt {attempt} failed ({resp.status_code}), retrying...")
        time.sleep(2 * attempt)
    resp.raise_for_status()
 
 
def main():
    print(f"Fetching weather for ({LATITUDE}, {LONGITUDE}) "
          f"{START_DATE} -> {END_DATE} ...")
    data = fetch_weather(LATITUDE, LONGITUDE, START_DATE, END_DATE, HOURLY_VARS)
 
    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"]) 
 
    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour
 
    df.to_parquet(OUTPUT_PATH, index=False)
    print(f"Saved {len(df):,} hourly rows -> {OUTPUT_PATH}")
    print(df.head())
    print("\nMissing values per column:")
    print(df.isna().sum())
 
 
if __name__ == "__main__":
    main()