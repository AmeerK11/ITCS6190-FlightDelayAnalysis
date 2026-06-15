import os
os.environ["PYSPARK_PYTHON"] = r"C:\Users\Ameer\AppData\Local\Programs\Python\Python314\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\Ameer\AppData\Local\Programs\Python\Python314\python.exe"
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import pandas as pd
import time

# ── 1. Start Spark ────────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("FlightDelayStreaming") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("✓ Spark session started")
print("  Simulating Spark Structured Streaming via micro-batch loop\n")

# ── 2. Load full cleaned dataset ──────────────────────────────────────────────
df_full = pd.read_csv("data/processed/flights_clean.csv")
total_rows = len(df_full)
print(f"✓ Loaded {total_rows:,} rows for streaming simulation")

# ── 3. Micro-batch streaming simulation ───────────────────────────────────────
BATCH_SIZE = 1000
NUM_BATCHES = 5
all_results = []

for batch_num in range(1, NUM_BATCHES + 1):
    start = (batch_num - 1) * BATCH_SIZE
    end   = start + BATCH_SIZE
    batch_pd = df_full.iloc[start:end]

    # Convert batch to Spark DataFrame
    batch_df = spark.createDataFrame(batch_pd)
    batch_df.createOrReplaceTempView("batch")

    # Aggregate: delay stats per airline for this batch
    result = spark.sql("""
        SELECT AIRLINE_CODE,
               COUNT(*) AS flight_count,
               ROUND(AVG(ARR_DELAY), 2) AS avg_arr_delay,
               ROUND(AVG(DELAYED) * 100, 2) AS delay_rate_pct
        FROM batch
        GROUP BY AIRLINE_CODE
        ORDER BY delay_rate_pct DESC
    """)

    print(f"── Micro-batch {batch_num} (rows {start}–{end}) ──")
    result.show(truncate=False)
    
    batch_result = result.toPandas()
    batch_result.insert(0, 'batch', batch_num)
    all_results.append(batch_result)    
    
    time.sleep(2)
    
# ── 4. Save results ───────────────────────────────────────────────────────────
os.makedirs("docs", exist_ok=True)
pd.concat(all_results).to_csv("docs/streaming_results.csv", index=False)
print("✓ Streaming results saved to docs/streaming_results.csv")


spark.stop()
print("✓ Streaming simulation complete.")