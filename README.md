# NJ Transit Train Delay Predictor

Predicts whether an NJ Transit / Amtrak (NEC) train will be delayed — and by
how many minutes — from line, station, time of day, day of week, and weather.

**Data:** NJ Transit + Amtrak (NEC) Rail Performance (Kaggle, ~150k+ trips,
Mar 2018 – May 2020), scraped from NJ Transit's DepartureVision service.

## Status
- [ ] Data profiled — run `data_quality_check.py`
- [ ] Data cleaned
- [ ] Features engineered
- [ ] Baseline model running end-to-end
- [ ] Gradient-boosting model beats baseline
- [ ] Evaluation + feature importance
- [ ] README writeup done

## Structure
```
.
├── data/                  # raw Kaggle CSVs (git-ignore this folder)
├── data_quality_check.py  # run FIRST — profiles the raw data
├── clean.py               # (you write) load + clean -> data/clean.parquet
├── features.py            # (you write) feature engineering
├── model.py               # (you write) baseline + gradient boosting + metrics
└── README.md
```


## Notes on the raw data
- The download includes separate **"invalid trains"** files — read those first;
  they're the publisher telling you which rows they already flagged as bad.
- Source is a scraper reading a live-status screen, so expect gaps, some
  duplicates, and timestamp quirks. That's normal for scraped data.
- The **Mar–May 2020** tail is the COVID collapse — a regime change, not dirt.
  Most likely you exclude it and say so.

## 1st Hypothesis

I believe that weather can significantly help with predicting whether NJ Transit rails will
be late to their designated station. Bad weather causes unwanted debris on the tracks which
can force trains to slow or come to a stop, ultimately causing them to be delayed. Although
this most likely won't be the only factor to why NJ transit is late, I think it would be 
a good starting point on creating a delay prediction model for NJ Transit lines.

## Data quality summary

The dataset is 6.37M stop-level records (one row per train per station) 
across 27 monthly files, Mar 2018–May 2020, with a consistent schema and 
zero duplicates. Two invalid_trains files use a different schema and are 
excluded from the modeling table. ~9.6% of rows lack scheduled_time/delay_minutes 
and are dropped (no computable target); cancellations (~1.3%) are kept as a separate 
signal. The delay target is reliable — no negatives, no sentinels, 45/5.76M rows 
above 180 min — but right-skewed (mean 4.2, median 2.3). COVID months (Apr–May 2020) 
show a sharp volume drop and are excluded, leaving continuous pre-pandemic data through Feb 2020.

## Results
<!-- baseline score, model score, top features, one real insight -->
=== BASELINE ===
Accuracy: 0.7349
(precision/recall/F1 are 0 - it never predicts a delay)


## ======= MODEL TESTING WITH & WITHOUT WEATHER FEATURES LGMCLASSIFIER USING CLASS_WEIGHT = "BALANCED" =========


## 2nd Hypothesis

After analyzing our incorporated weather data into features.py, it is evident
that weather is not a much of a major feature utilized by the prediction model.
What are major features would be scheduled time (hour), station the train is coming from,
and it's line.

Due to these factors, and a realization that NJ Transit often gives higher priority to
Amtrak rails (which has been filtered out of our dataFrame), I believe that maybe we could
improve the prediction model by knowing which Amtrak rails are scheduled and whether they
overlap with NJ Transit schedules.

I won't be removing weather data just yet, but it is a possibility that it will be removed in
the future due to its poor performance on the prediction model. Our model has slighly better performance
without the weather data.


## Resume pitch (draft)
<!-- e.g. "Built an end-to-end ML pipeline predicting NJ Transit delays across
     150k+ real trips; engineered temporal + weather features; a LightGBM model
     reached [metric], beating the baseline by [X]; identified [top driver] as
     the strongest predictor of delay." -->
