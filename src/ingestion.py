from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import IntegerType
import os

# ── 1. Start Spark ──────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("FlightDelayIngestion") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("✓ Spark session started")

# ── 2. Load CSV ───────────────────────────────────────────────────────────────
RAW_PATH = "data/raw/flights_sample_3m.csv"

print(f"Loading {RAW_PATH} ...")
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("nullValue", "") \
    .csv(RAW_PATH)

print(f"✓ Raw row count: {df_raw.count():,}")

# ── 3. Clean ──────────────────────────────────────────────────────────────────
df_clean = df_raw.dropna(subset=["FL_DATE", "AIRLINE_CODE", "ORIGIN", "DEST",
                                  "DEP_DELAY", "ARR_DELAY"])

df_clean = df_clean.withColumn(
    "DELAYED",
    when(col("ARR_DELAY") >= 15, 1).otherwise(0)
)

df_clean = df_clean.withColumn(
    "DEP_HOUR",
    (col("CRS_DEP_TIME") / 100).cast(IntegerType())
)

print(f"✓ Clean row count: {df_clean.count():,}")

# ── 4. Quick sanity check ─────────────────────────────────────────────────────
print("\n── Schema ──")
df_clean.printSchema()

print("\n── Sample rows ──")
df_clean.select("FL_DATE", "AIRLINE_CODE", "ORIGIN", "DEST",
                "DEP_DELAY", "ARR_DELAY", "DELAYED", "DEP_HOUR").show(5)

# ── 5. Save using pandas (avoids Windows winutils issue) ──────────────────────
os.makedirs("data/processed", exist_ok=True)
OUTPUT_PATH = "data/processed/flights_clean.csv"

print("\nSaving to disk via pandas (this may take a minute)...")
df_clean.toPandas().to_csv(OUTPUT_PATH, index=False)
print(f"✓ Saved cleaned data to {OUTPUT_PATH}")

spark.stop()
print("\n✓ Done.")