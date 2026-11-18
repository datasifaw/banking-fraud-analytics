# Banking Fraud Analytics - Dataset Documentation

## 1. Project Information

Project Name: Banking Fraud Analytics

Jira Ticket: AZ-2

Sprint: Sprint 0 - Initialization

Git Branch: feature/AZ-2-description

Project Type: Data Engineering and Business Intelligence

---

## 2. Dataset Source

Dataset Name: Credit Card Fraud Detection

Platform: Kaggle

Source URL:
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

The dataset contains historical anonymized credit card
transactions.

The objective is to analyze fraudulent transactions
and build a banking fraud analytics dashboard.

---

## 3. Dataset Characteristics

File Name: creditcard.csv

File Format: CSV

File Location: data/creditcard.csv

File Size: 143.84 MiB (PowerShell measurement)

Total Transactions: 284807

Total Columns: 31

The dataset contains transactions labeled as
legitimate or fraudulent.

The number of fraudulent transactions will be
verified during the Python data quality analysis.

---

## 4. Dataset Schema

The dataset contains the following columns:

### Time

Type: Numeric

Description:
Elapsed time in seconds between each transaction
and the first transaction in the dataset.

### V1 to V28

Type: Numeric

Description:
Anonymized numerical features obtained through
Principal Component Analysis (PCA).

These variables do not expose the original
transaction attributes.

### Amount

Type: Numeric

Description:
Transaction amount.

This column will be used for financial analysis,
amount distributions and fraud-related KPIs.

### Class

Type: Integer

Description:
Transaction classification.

Expected values:

0 = Legitimate transaction

1 = Fraudulent transaction

These values will be checked during data validation.

---

## 5. Data Quality Checks

Checks completed during Sprint 0:

- CSV file exists locally.
- File size verified.
- Total row count verified: 284807.
- Total column count verified: 31.
- Column names verified against the expected schema.
- CSV exclusion through .gitignore confirmed.
- Git working directory verified as clean.

Checks planned for the Python pipeline:

- Missing values.
- Duplicate rows.
- Invalid numeric values.
- Invalid Class values.
- Negative transaction amounts.
- Fraud and legitimate transaction counts.
- Fraud percentage.
- Statistical distributions.

The current checks do not guarantee that every
record is valid.

---

## 6. Data Security

The CSV dataset is stored locally.

The raw CSV must not be committed to GitHub.

The .gitignore configuration excludes local
dataset files.

Credentials and secrets must never be committed.

Only project code, SQL scripts, documentation
and approved analytical outputs will be versioned.

---

## 7. Target Data Architecture

Kaggle CSV
    |
    v
Python / Pandas
    |
    v
Cleaned Dataset
    |
    v
Google BigQuery Sandbox
    |
    v
SQL Analytical Queries
    |
    v
Aggregated CSV Exports
    |
    v
Google Data Studio
    |
    v
Banking Fraud Dashboard

---

## 8. Planned Business KPIs

The project will calculate:

1. Total number of transactions.

2. Total number of fraudulent transactions.

3. Fraud rate.

4. Total amount of fraudulent transactions.

5. Average fraudulent transaction amount.

6. Fraud distribution by transaction amount.

7. Fraud distribution over elapsed time.

---

## 9. Project Constraints

- Google BigQuery Sandbox without billing.
- No bank card required.
- No paid Cloud subscriptions.
- Dashboard based on exported analytical CSV files.
- No real-time ingestion in the initial version.
- No Machine Learning in the initial version.
- Historical anonymized dataset only.

---

## 10. Current Status

Sprint 0 - Dataset preparation.

Completed:
- Dataset downloaded.
- Dataset file structure verified.
- Column names validated.
- Git exclusion confirmed.

Pending:
- Python data quality analysis.
- Data transformations.
- BigQuery ingestion.
- SQL analytical queries.
- Data Studio dashboard.
