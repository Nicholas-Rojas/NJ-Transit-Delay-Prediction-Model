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

## Plan (weekend MVP)
1. **Profile + clean** — know the data, drop junk, decide how to treat cancellations.
2. **Features** — hour, day-of-week, month, line, station; then join your weather data.
3. **Baseline** — "always on time" or mean-delay. This is the number to beat.
4. **Model** — LightGBM/XGBoost: classifier (delayed yes/no) or regressor (minutes).
5. **Evaluate** — accuracy/F1 or MAE vs. baseline, confusion matrix, feature importance.

## The one hard rule for this build
**Get a dumb baseline model running end-to-end BEFORE perfecting the clean.**
Working-but-imperfect beats flawless-but-unfinished. Box the cleaning; close the box.

## Notes on the raw data
- The download includes separate **"invalid trains"** files — read those first;
  they're the publisher telling you which rows they already flagged as bad.
- Source is a scraper reading a live-status screen, so expect gaps, some
  duplicates, and timestamp quirks. That's normal for scraped data.
- The **Mar–May 2020** tail is the COVID collapse — a regime change, not dirt.
  Most likely you exclude it and say so.

## Data quality summary
<!-- After running the profiler, write 3–4 sentences here:
     row count, schema consistency, what missingness means, dups removed,
     how you handled the COVID months, target reliability. Resume asset. -->

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

## Resume pitch (draft)
<!-- e.g. "Built an end-to-end ML pipeline predicting NJ Transit delays across
     150k+ real trips; engineered temporal + weather features; a LightGBM model
     reached [metric], beating the baseline by [X]; identified [top driver] as
     the strongest predictor of delay." -->
