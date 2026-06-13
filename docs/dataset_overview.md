# Dataset Overview

| Field | Details |
|-------|---------|
| Name | Flight Delay and Cancellation Dataset (2019–2023) |
| File | flights_sample_3m.csv |
| Source | https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023 |
| Size | 3,000,000 rows, 32 columns |
| License | Public domain (Kaggle) |

## Key Columns

| Column | Type | Description |
|--------|------|-------------|
| FL_DATE | date | Flight date |
| AIRLINE_CODE | string | 2-letter carrier code |
| ORIGIN / DEST | string | Origin and destination airport codes |
| DEP_DELAY | double | Departure delay in minutes |
| ARR_DELAY | double | Arrival delay in minutes |
| CANCELLED | double | 1 if cancelled, 0 otherwise |
| DELAY_DUE_CARRIER | double | Delay minutes due to carrier |
| DELAY_DUE_WEATHER | double | Delay minutes due to weather |
| DELAY_DUE_NAS | double | Delay minutes due to NAS |
| DELAY_DUE_LATE_AIRCRAFT | double | Delay minutes due to late aircraft |

## Preprocessing
- Dropped rows missing FL_DATE, AIRLINE_CODE, ORIGIN, DEST, DEP_DELAY, or ARR_DELAY
- Raw: 3,000,000 rows → Clean: 2,913,802 rows
- Added binary label `DELAYED` (1 if ARR_DELAY ≥ 15 min, else 0)
- Added `DEP_HOUR` feature extracted from CRS_DEP_TIME
- Raw data stored locally at `data/raw/` and excluded from version control