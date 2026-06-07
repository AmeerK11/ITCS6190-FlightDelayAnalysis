from pyspark.sql import SparkSession
import os

# ── 1. Start Spark ──────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("FlightDelaySQL") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("✓ Spark session started")

# ── 2. Load cleaned data ──────────────────────────────────────────────────────
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("data/processed/flights_clean.csv")

df.createOrReplaceTempView("flights")
print(f"✓ Loaded {df.count():,} rows into Spark SQL view")

# ── Query 1: Top 10 airlines by average arrival delay ────────────────────────
print("\n── Q1: Top Airlines by Avg Arrival Delay ──")
q1 = spark.sql("""
    SELECT AIRLINE_CODE, AIRLINE,
           ROUND(AVG(ARR_DELAY), 2) AS avg_arr_delay,
           COUNT(*) AS total_flights
    FROM flights
    GROUP BY AIRLINE_CODE, AIRLINE
    ORDER BY avg_arr_delay DESC
    LIMIT 10
""")
q1.show(truncate=False)

# ── Query 2: Top 10 routes by average arrival delay ──────────────────────────
print("\n── Q2: Top Routes by Avg Arrival Delay ──")
q2 = spark.sql("""
    SELECT ORIGIN, DEST,
           ROUND(AVG(ARR_DELAY), 2) AS avg_arr_delay,
           COUNT(*) AS total_flights
    FROM flights
    GROUP BY ORIGIN, DEST
    HAVING COUNT(*) > 100
    ORDER BY avg_arr_delay DESC
    LIMIT 10
""")
q2.show(truncate=False)

# ── Query 3: Delay rate by departure hour and day of week ────────────────────
print("\n── Q3: Delay Rate by Hour and Day of Week ──")
q3 = spark.sql("""
    SELECT DEP_HOUR,
           DAYOFWEEK(FL_DATE) AS day_of_week,
           ROUND(AVG(DELAYED) * 100, 2) AS delay_rate_pct,
           ROUND(AVG(DEP_DELAY), 2) AS avg_dep_delay
    FROM flights
    GROUP BY DEP_HOUR, DAYOFWEEK(FL_DATE)
    ORDER BY delay_rate_pct DESC
    LIMIT 10
""")
q3.show(truncate=False)

# ── Query 4: Worst airports by on-time performance and delay causes ───────────
print("\n── Q4: Worst Airports by On-Time Performance ──")
q4 = spark.sql("""
    SELECT ORIGIN,
           ROUND(AVG(DELAYED) * 100, 2) AS delay_rate_pct,
           ROUND(AVG(DELAY_DUE_CARRIER), 2) AS avg_carrier_delay,
           ROUND(AVG(DELAY_DUE_WEATHER), 2) AS avg_weather_delay,
           ROUND(AVG(DELAY_DUE_NAS), 2) AS avg_nas_delay,
           ROUND(AVG(DELAY_DUE_LATE_AIRCRAFT), 2) AS avg_late_aircraft_delay,
           COUNT(*) AS total_flights
    FROM flights
    GROUP BY ORIGIN
    HAVING COUNT(*) > 500
    ORDER BY delay_rate_pct DESC
    LIMIT 10
""")
q4.show(truncate=False)

# ── Query 5: Pre-COVID vs Post-COVID delay patterns ──────────────────────────
print("\n── Q5: Pre-COVID (2019) vs Post-COVID (2022-2023) Delay Patterns ──")
q5 = spark.sql("""
    SELECT YEAR(FL_DATE) AS year,
           ROUND(AVG(ARR_DELAY), 2) AS avg_arr_delay,
           ROUND(AVG(DEP_DELAY), 2) AS avg_dep_delay,
           ROUND(AVG(DELAYED) * 100, 2) AS delay_rate_pct,
           COUNT(*) AS total_flights
    FROM flights
    WHERE YEAR(FL_DATE) IN (2019, 2020, 2021, 2022, 2023)
    GROUP BY YEAR(FL_DATE)
    ORDER BY year
""")
q5.show(truncate=False)

spark.stop()
print("\n✓ All SQL queries complete.")