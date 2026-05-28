# Flight Delay Analysis & Prediction
### ITCS 6190 – Cloud Computing for Data Analysis | Summer 2026

## Project Overview
An end-to-end big data analytics pipeline built with Apache Spark to analyze
and predict U.S. domestic flight delays. The pipeline covers data ingestion,
SQL-based analysis, real-time streaming simulation, and machine learning 
all developed using the Apache Spark ecosystem.

## Student
**Ameer Khan** — Individual Submission

## Dataset
| Field       | Details |
|------------|---------|
| Name        | Flight Delay and Cancellation Dataset (2019–2023) |
| File        | flights_sample_3m.csv |
| Source      | https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023 |
| Size        | ~3,000,000 rows, 32 columns |
| Description | U.S. domestic flight records including routes, departure/arrival times, delay durations, delay causes, and cancellation codes |

## Analytical Questions
1. Which airlines and routes have the highest average arrival delay?
2. What times of day and days of week are most correlated with departure delays?
3. Which origin airports have the worst on-time performance and what are the dominant delay causes?
4. Can we predict whether a flight will be delayed ≥15 minutes based on carrier, origin airport, scheduled departure hour, day of week, and month?
5. How did delay patterns change from pre-COVID (2019) to post-COVID (2022–2023)?

## Pipeline Components
| Component       | Description |
|----------------|-------------|
| Structured APIs | Ingest and clean CSV data; apply transformations and aggregations |
| Spark SQL       | Query delay patterns by airline, airport, time of day, and year |
| Streaming       | Simulate real-time flight arrivals using Spark Structured Streaming |
| MLlib           | Binary classification to predict flight delay ≥15 min (Logistic Regression + Random Forest); evaluated with accuracy, precision, recall, F1, and AUC-ROC |

## Repository Structure
├── data/               
├── docs/               
├── notebooks/          
├── src/                
├── tests/              
├── requirements.txt    
├── run.sh              
└── Makefile            
