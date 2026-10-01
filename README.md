# NJ Transit Train Delay Predictor

Predicts whether an NJ Transit train will be delayed by more than 5 minutes,
using line, station, time of day, day of week, and the train's own delay from
its previous stop.

**Headline Results:**
A baseline model predicts 0 delays with ~0.73 accuracy by always guessing on-time.
The final model catches ~85% of delays (F1 ~0.80), with the strongest driver being
cascading delay — a train late at its previous stop.

**Data:**
NJ Transit + Amtrak (NEC) Rail Performance (Kaggle), ~6.37M stop-level
records (one row per train per station), Mar 2018 – May 2020, scraped from NJ
Transit's DepartureVision service. ~5.3M rows used after cleaning.

**Link to Date**
https://www.kaggle.com/datasets/pranavbadami/nj-transit-amtrak-nec-performance/data



## Results

Target: `delayed = delay_minutes > 5`, per stop-level row. Evaluation uses a
time-based split — trained on Mar 2018 – Oct 2019, tested on Nov 2019 – Feb 2020.
All models use `class_weight='balanced'` to counter the 73/27 class imbalance.

| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|-----|
| Baseline (always "on-time") | 0.735 | 0.00 | 0.00 | 0.00 |
| When/where (line, station, hour, day) | 0.560 | 0.356 | 0.819 | 0.497 |
| + Weather | 0.573 | 0.359 | 0.779 | 0.491 |
| + Weather + Amtrak | 0.572 | 0.359 | 0.783 | 0.492 |
| + Previous delay | 0.887 | 0.754 | 0.849 | 0.799 |
| + Previous delay + Weather + Amtrak | 0.886 | 0.752 | 0.848 | 0.797 |

**Highlights:**

1. External context such as weather conditions and Amtrak trains scheduled within the region
   had little to no effect on our model.

2. Cascading delay had the greatest change within the model, jumping F1 from 0.50 to 0.80.
   Again, adding weather and Amtrak still had no major change to the model — confirming their
   weakness to the model.

**Feature importance — final model:**

```
from             2891
prev_delay       1034
stop_sequence     789
hour              593
line              324
month             189
dayofweek         180
```

## Hypotheses Tested

Project went through 4 hypotheses, with the final model only keeping those with major effects.

1. **Weather (original):**
   Using weather conditions such as rain, snow and their severity as key indicators for delay.
   The results were negligible as weather features ranked at the bottom of importance.

2. **Amtrak shared track:**
   NJ Transit and Amtrak trains share railways in the NEC rails, with Amtrak getting priority over
   NJ Transit rails. Used count of Amtrak trains present at a station in a given hour by reusing Amtrak
   rows already in the raw data. Results were negligible, and only ever non-zero on the ~8 NEC stations.

   Note: Dataset did not contain the scheduled times of these trains at each station, thus halting further
   experimentation with Amtrak data.

3. **Cascading delay:**
   When a train has its first delay, it can be used as a key indicator for it being late to its next
   station. It cannot make up the lost minutes to keep on track with its schedule. The results were
   decisive and more than doubled F1.

4. **All features combined:**
   Speculated that with cascading delays, it can be more precise with the Amtrak and weather data. The
   results didn't agree and had negligible change.

**No data leakage:**
`prev_delay` uses the previous row's stop delay, which a real system would already know.
This was verified by inspecting that `stop_sequence == 1` rows have `prev_delay = NaN` and
every later row's `prev_delay` equals the prior row's `delay_minutes`.

## Data quality summary

The dataset is 6.37M stop-level records (one row per train per station)
across 27 monthly files, Mar 2018–May 2020, with a consistent schema and
zero duplicates. Two invalid_trains files use a different schema and are
excluded from the modeling table. ~9.6% of rows lack scheduled_time/delay_minutes
and are dropped (no computable target); cancellations (~1.3%) are kept as a separate
signal. The delay target is reliable — no negatives, no sentinels, 45/5.76M rows
above 180 min — but right-skewed (mean 4.2, median 2.3). COVID months (Apr–May 2020)
show a sharp volume drop and are excluded, leaving continuous pre-pandemic data through Feb 2020.

## Limitations & Future Work

**Precision ceiling:**
Much of what causes delay — such as NJ Transit's aging infrastructure, which allows for
mechanical faults, signal failures, etc. — is NOT recorded in this dataset, and
no credible or sufficient dataset could be found to effectively use in this model.

**Single weather point:**
Weather was used in one location (Newark) as a corridor-wide proxy. Using exact
weather conditions for all stations is untested, but given the negligible effects
with Newark weather, it is unlikely to change the conclusion.

**`prev_delay` timing:**
The feature uses the previous stop's recorded delay. A strict real-time deployment
would use only delays known at inference time; the backward-looking window here is
a fair but slightly idealized version of that.

**Next steps:**
Add richer upstream features, threshold tuning via prediction probability
(`predict_proba`) to dial the precision/recall tradeoff, and newer post-2020 data via NJ
Transit's real-time developer feed.

## Pipeline / How to Run

```
data/
  raw/        # Kaggle CSVs (git-ignored)
  processed/  # generated parquets (git-ignored)
```

```bash
pip install pandas lightgbm scikit-learn pyarrow requests

# 1. Download the Kaggle dataset into data/raw/
python data_quality_check.py   # profile the raw data (optional, run once)
python clean.py                 # -> data/processed/clean.parquet
python weather.py               # -> data/processed/weather.parquet
python amtrak.py                # -> data/processed/amtrak_congestion.parquet
python features.py              # -> data/processed/features.parquet
python model.py                 # trains + prints the results table above
```

## Files

| File | Role |
|------|------|
| `data_quality_check.py` | Profiles raw data before modeling |
| `clean.py` | Filters to NJ Transit, drops null targets, cuts COVID tail, builds `delayed` |
| `weather.py` | Pulls historical hourly weather (Open-Meteo archive) |
| `amtrak.py` | Builds Amtrak station-hour congestion counts |
| `features.py` | Time features + weather join + Amtrak join + `prev_delay` |
| `model.py` | Baseline + LightGBM, time-based split, metrics, feature importance |

## Tech Stack

Python · pandas · LightGBM · scikit-learn · pyarrow · Open-Meteo API