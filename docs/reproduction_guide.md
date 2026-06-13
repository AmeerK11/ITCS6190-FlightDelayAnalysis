# Reproduction Guide
## Requirements
- Python 3.9+
- Java 17
- PySpark 4.x
- pandas, matplotlib, jupyter

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/AmeerK11/ITCS6190-FlightDelayAnalysis.git
cd ITCS6190-FlightDelayAnalysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the dataset
Download `flights_sample_3m.csv` from Kaggle:
https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023

Place it at:
data/raw/flights_sample_3m.csv

### 4. Windows-specific setup
If running on Windows, set the PYSPARK_PYTHON environment variable:
```bash
set PYSPARK_PYTHON=C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python314\python.exe
```

---

## Run the Full Pipeline

### Option 1 — Single command
```bash
make run
```

### Option 2 — Bash
```bash
bash run.sh
```

### Option 3 — Individual scripts
```bash
py src/ingestion.py       # Step 1: Ingest and clean data
py src/sql_analysis.py    # Step 2: Spark SQL analysis
py src/streaming.py       # Step 3: Streaming simulation
py src/ml_model.py        # Step 4: Train ML models
```

---

## Expected Output

| Step | Output |
|------|--------|
| Ingestion | `data/processed/flights_clean.csv` (2,913,802 rows) |
| SQL Analysis | 5 query results printed to console |
| Streaming | 5 micro-batch results printed to console |
| ML Model | Model comparison table with AUC-ROC, Accuracy, Precision, Recall, F1 |

---

## EDA Notebook
To run the EDA notebook:
```bash
jupyter notebook notebooks/eda.ipynb
```