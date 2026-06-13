# Methodology

## Pipeline Overview

The pipeline consists of four stages executed in sequence:
1. Data Ingestion & Cleaning
2. Spark SQL Analysis
3. Streaming Simulation
4. MLlib Machine Learning

---

## 1. Data Ingestion (`src/ingestion.py`)

Loaded the raw CSV using the Spark DataFrame Structured API with schema inference and null value handling. Applied null filtering on six key columns and engineered two new features:
- `DELAYED` — binary label, 1 if ARR_DELAY ≥ 15 min, else 0
- `DEP_HOUR` — integer hour extracted from CRS_DEP_TIME (e.g. 830 → 8)

Used pandas `to_csv()` for file output to work around a Windows winutils limitation with Spark's native file writer.

---

## 2. Exploratory Data Analysis (`notebooks/eda.ipynb`)

Performed EDA using pandas and matplotlib on the cleaned dataset:
- Null counts per column
- Delay rate by airline
- Average arrival delay by departure hour
- Average arrival delay by day of week
- Top 10 airports by average arrival delay
- Overall delayed vs on-time distribution

---

## 3. Spark SQL Analysis (`src/sql_analysis.py`)

Registered the cleaned dataset as a Spark SQL temp view and executed 5 queries:

| Query | Description |
|-------|-------------|
| Q1 | Top airlines by average arrival delay |
| Q2 | Top routes by average arrival delay (min 100 flights) |
| Q3 | Delay rate by departure hour and day of week |
| Q4 | Worst airports by on-time performance with delay cause breakdown |
| Q5 | Pre-COVID (2019) vs post-COVID (2022–2023) delay trends by year |

---

## 4. Streaming Simulation (`src/streaming.py`)

Simulated Spark Structured Streaming using a micro-batch loop. Each iteration:
1. Reads a 1,000-row slice of the cleaned dataset
2. Converts it to a Spark DataFrame
3. Registers it as a SQL temp view
4. Computes flight count, avg arrival delay, and delay rate per airline
5. Prints results to console

Ran 5 batches to demonstrate real-time aggregation behavior. Used `PYSPARK_PYTHON` environment variable to resolve Python worker connection issues on Windows.

---

## 5. MLlib Model (`src/ml_model.py`)

### Features
| Feature | Type | Description |
|---------|------|-------------|
| AIRLINE_CODE | categorical | StringIndexed to numeric |
| DEP_HOUR | integer | Scheduled departure hour |
| DISTANCE | double | Route distance in miles |
| CRS_ELAPSED_TIME | double | Scheduled flight duration in minutes |

### Models
- **Logistic Regression** — maxIter=10, binary classification
- **Random Forest** — numTrees=50, seed=42

### Evaluation Metrics
- AUC-ROC, Accuracy, Weighted Precision, Weighted Recall, F1 Score

### Train/Test Split
- 80% training (2,331,480 rows) / 20% test (582,322 rows), seed=42