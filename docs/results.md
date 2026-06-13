# Results

## EDA Findings

### Delay Distribution
- 81.7% of flights are on time (2,379,939 flights)
- 18.3% of flights are delayed ≥15 min (533,863 flights)

### Delay Rate by Airline
| Airline | Delay Rate |
|---------|-----------|
| JetBlue (B6) | 27.00% |
| Frontier (F9) | 26.65% |
| Allegiant (G4) | 26.09% |
| Spirit (NK) | 22.12% |
| Delta (DL) | 14.41% |
| Hawaiian (HA) | 16.38% |

### Delay by Time
- Delays increase steadily throughout the day, peaking in evening hours (7–9pm)
- Early morning flights (5–6am) have the lowest average delay
- Friday has the highest average arrival delay by day of week

### Worst Airports by Avg Arrival Delay
| Airport | Avg Delay (min) |
|---------|----------------|
| PPG | 56.5 |
| SMX | 37.9 |
| PSM | 31.1 |
| PGV | 24.8 |
| HGR | 24.8 |

---

## Spark SQL Findings

### Q1 — Top Airlines by Avg Arrival Delay
- Allegiant Air (G4): 13.28 min avg arrival delay
- JetBlue (B6): 12.28 min
- Frontier (F9): 11.10 min

### Q2 — Top Routes by Avg Arrival Delay
- ABQ→JFK: 40.1 min avg (worst route)
- ACK→LGA: 38.9 min
- ASE→ORD: 38.5 min

### Q3 — Delay Rate by Hour and Day
- 3am Tuesday flights: 43% delay rate (highest)
- Evening flights (7–9pm) on weekdays consistently above 27%

### Q4 — Worst Airports by On-Time Performance
- BQN: 32.69% delay rate
- USA: 32.42%
- ASE: 29.54%

### Q5 — COVID Impact on Delays
| Year | Avg Arrival Delay | Delay Rate |
|------|-------------------|-----------|
| 2019 | 5.31 min | 19.03% |
| 2020 | -5.01 min | 9.80% |
| 2021 | 3.10 min | 17.24% |
| 2022 | 6.91 min | 21.04% |
| 2023 | 9.37 min | 23.03% |

2020 had negative average delay due to COVID-reduced air traffic. Post-COVID delays are worse than pre-COVID, with 2023 being the worst year in the dataset.

---

## ML Model Results

| Metric | Logistic Regression | Random Forest |
|--------|-------------------|---------------|
| AUC-ROC | 0.6090 | 0.6061 |
| Accuracy | 0.8166 | 0.8166 |
| Precision | 0.6668 | 0.6668 |
| Recall | 0.8166 | 0.8166 |
| F1 Score | 0.7341 | 0.7341 |

Both models achieved similar performance. The 81.7% accuracy reflects the class imbalance in the dataset. The AUC-ROC of ~0.61 indicates the models perform better than random guessing at distinguishing delayed vs on-time flights. Logistic Regression marginally outperforms Random Forest on AUC-ROC (0.6090 vs 0.6061).

### Visualizations
See `/docs/` for charts:
- `delay_distribution.png` — delayed vs on-time breakdown
- `delay_by_hour.png` — avg arrival delay by departure hour
- `delay_by_day.png` — avg arrival delay by day of week
- `delay_by_airport.png` — top 10 airports by avg arrival delay