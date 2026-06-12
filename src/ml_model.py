import os
os.environ["PYSPARK_PYTHON"] = r"C:\Users\Ameer\AppData\Local\Programs\Python\Python314\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\Ameer\AppData\Local\Programs\Python\Python314\python.exe"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

# ── 1. Start Spark ────────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("FlightDelayMLlib") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("✓ Spark session started")

# ── 2. Load cleaned data ──────────────────────────────────────────────────────
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("data/processed/flights_clean.csv")

print(f"✓ Loaded {df.count():,} rows")

# ── 3. Feature engineering ────────────────────────────────────────────────────
# Encode AIRLINE_CODE as numeric index
indexer = StringIndexer(inputCol="AIRLINE_CODE", outputCol="AIRLINE_IDX", handleInvalid="keep")

# Assemble feature vector
assembler = VectorAssembler(
    inputCols=["AIRLINE_IDX", "DEP_HOUR", "DISTANCE", "CRS_ELAPSED_TIME"],
    outputCol="features",
    handleInvalid="skip"
)

# ── 4. Prepare label column ───────────────────────────────────────────────────
df = df.withColumn("label", col("DELAYED").cast("double"))

# ── 5. Train/test split ───────────────────────────────────────────────────────
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
print(f"✓ Train: {train_df.count():,} rows | Test: {test_df.count():,} rows")

# ── 6. Logistic Regression ────────────────────────────────────────────────────
print("\n── Training Logistic Regression ──")
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=10)
lr_pipeline = Pipeline(stages=[indexer, assembler, lr])
lr_model = lr_pipeline.fit(train_df)
lr_preds = lr_model.transform(test_df)

# Evaluate LR
binary_eval = BinaryClassificationEvaluator(labelCol="label")
multi_eval  = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")

lr_auc       = binary_eval.evaluate(lr_preds)
lr_accuracy  = multi_eval.evaluate(lr_preds, {multi_eval.metricName: "accuracy"})
lr_precision = multi_eval.evaluate(lr_preds, {multi_eval.metricName: "weightedPrecision"})
lr_recall    = multi_eval.evaluate(lr_preds, {multi_eval.metricName: "weightedRecall"})
lr_f1        = multi_eval.evaluate(lr_preds, {multi_eval.metricName: "f1"})

print(f"  AUC-ROC:   {lr_auc:.4f}")
print(f"  Accuracy:  {lr_accuracy:.4f}")
print(f"  Precision: {lr_precision:.4f}")
print(f"  Recall:    {lr_recall:.4f}")
print(f"  F1 Score:  {lr_f1:.4f}")

# ── 7. Random Forest ──────────────────────────────────────────────────────────
print("\n── Training Random Forest ──")
rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=50, seed=42)
rf_pipeline = Pipeline(stages=[indexer, assembler, rf])
rf_model = rf_pipeline.fit(train_df)
rf_preds = rf_model.transform(test_df)

# Evaluate RF
rf_auc       = binary_eval.evaluate(rf_preds)
rf_accuracy  = multi_eval.evaluate(rf_preds, {multi_eval.metricName: "accuracy"})
rf_precision = multi_eval.evaluate(rf_preds, {multi_eval.metricName: "weightedPrecision"})
rf_recall    = multi_eval.evaluate(rf_preds, {multi_eval.metricName: "weightedRecall"})
rf_f1        = multi_eval.evaluate(rf_preds, {multi_eval.metricName: "f1"})

print(f"  AUC-ROC:   {rf_auc:.4f}")
print(f"  Accuracy:  {rf_accuracy:.4f}")
print(f"  Precision: {rf_precision:.4f}")
print(f"  Recall:    {rf_recall:.4f}")
print(f"  F1 Score:  {rf_f1:.4f}")

# ── 8. Summary ────────────────────────────────────────────────────────────────
print("\n── Model Comparison ──")
print(f"{'Metric':<12} {'Logistic Reg':>14} {'Random Forest':>14}")
print("-" * 42)
print(f"{'AUC-ROC':<12} {lr_auc:>14.4f} {rf_auc:>14.4f}")
print(f"{'Accuracy':<12} {lr_accuracy:>14.4f} {rf_accuracy:>14.4f}")
print(f"{'Precision':<12} {lr_precision:>14.4f} {rf_precision:>14.4f}")
print(f"{'Recall':<12} {lr_recall:>14.4f} {rf_recall:>14.4f}")
print(f"{'F1 Score':<12} {lr_f1:>14.4f} {rf_f1:>14.4f}")

spark.stop()
print("\n✓ ML model training complete.")