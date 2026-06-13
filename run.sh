#!/bin/bash
set -e

echo "=== Flight Delay Analysis Pipeline ==="
echo ""

echo "[1/4] Running data ingestion and cleaning..."
py src/ingestion.py

echo "[2/4] Running Spark SQL analysis..."
py src/sql_analysis.py

echo "[3/4] Running streaming simulation..."
py src/streaming.py

echo "[4/4] Running MLlib model training and evaluation..."
py src/ml_model.py

echo ""
echo "=== Pipeline complete ==="