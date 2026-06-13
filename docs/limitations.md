# Limitations

## Class Imbalance
81.7% of flights are on time, which means the ML models can achieve high accuracy by simply predicting "on time" for most flights. Techniques like SMOTE oversampling or class weighting would improve the model's ability to correctly identify delayed flights.

## Limited Feature Set
Only 4 features were used for ML (airline, departure hour, distance, elapsed time). Adding weather data, airport congestion levels, day of year, and holiday indicators would likely improve AUC-ROC significantly.

## Windows Environment Constraints
Two workarounds were required due to Windows lacking winutils:
- Spark's native file writer was replaced with pandas `to_csv()` for saving processed data
- Spark Structured Streaming's `readStream` API was replaced with a micro-batch loop using `spark.createDataFrame()`

Both workarounds produce equivalent results and would not be needed on Linux or macOS.

## Sample Dataset
The dataset is a 3 million row sample, not the full multi-year dataset. Results may differ on the complete dataset.

## No Hyperparameter Tuning
Models were trained with default or minimal parameters. Cross-validation and grid search would likely improve model performance.