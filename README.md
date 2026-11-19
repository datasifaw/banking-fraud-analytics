# Banking Fraud Analytics
 

## Project Overview

Banking Fraud Analytics is a Data Engineering and Business
Intelligence project focused on analyzing fraudulent credit
card transactions.

The objective is to build a complete analytics pipeline
using Python, Google BigQuery Sandbox, SQL and Data Studio.

## Business Objectives

- Analyze banking transaction volumes.
- Calculate the fraud rate.
- Analyze fraudulent transaction amounts.
- Identify fraud patterns by transaction amount.
- Visualize fraud distribution over elapsed time.

## Technologies

- Python
- Pandas
- Google Cloud Platform
- BigQuery Sandbox
- SQL
- Google Data Studio
- Git and GitHub
- GitHub Desktop
- Jira Scrum
- PowerShell
- Visual Studio Code

## Data Source

Credit Card Fraud Detection dataset from Kaggle.

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

The dataset contains anonymized historical credit card
transactions, including fraudulent and legitimate operations.

## Data Architecture

Kaggle CSV
    |
    v
Python / Pandas
    |
    v
Cleaned CSV
    |
    v
Google BigQuery Sandbox
    |
    v
SQL Analytics
    |
    v
Aggregated CSV Exports
    |
    v
Google Data Studio Dashboard

## Project Structure

banking-fraud-analytics/
|
|-- src/
|-- sql/
|-- data/
|-- dashboard/
|-- docs/
|-- .gitignore
|-- README.md

## Folder Descriptions

src/       Python data processing scripts

sql/       BigQuery SQL queries

data/      Local datasets, excluded from Git

dashboard/ Data Studio dashboard documentation

docs/      Technical and project documentation

## Scrum Organization

Sprint 0 - Project initialization
Sprint 1 - Data ingestion and preparation
Sprint 2 - SQL analytics and KPIs
Sprint 3 - Dashboard and final delivery

## Git Workflow

Main branch: main

Feature branches follow this convention:

feature/JIRA-KEY-description

Example:

feature/AZ-1-initialisation-projet

Each development task is tracked in Jira.

Commits and pushes are performed after validation.

## Cloud Cost Policy

This project uses BigQuery Sandbox without a billing account.

Data Studio uses CSV imports instead of a direct
billable BigQuery connector.

No bank card or paid Cloud subscription is required.

## Security

- Never commit credentials or API secrets.
- Never commit local transaction CSV files.
- Use anonymized public datasets only.
- Keep local Python environments outside version control.

## Project Status

Sprint 0 - Initialization in progress.
