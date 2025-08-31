# Store Sales Forecasting — DevOps Class Project

This repository contains the solution for the **Store Sales - Time Series Forecasting** competition hosted on [Kaggle](https://www.kaggle.com/competitions/store-sales-time-series-forecasting). The objective is to predict daily sales for a chain of stores using historical data, holidays, oil prices, and store metadata.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Data Description](#data-description)
- [Installation](#installation)
- [Usage](#usage)
- [Modeling Approach](#modeling-approach)
- [Results](#results)
- [DevOps Practices](#devops-practices)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

This project aims to forecast daily sales for multiple stores using:
- Historical sales data
- Holiday and event calendars
- Oil price fluctuations
- Store-level metadata

Developed as part of the **DevOps coursework**, the project emphasizes:
- Reproducible machine learning pipelines
- Collaborative development using Git and GitHub
- Automation and reproducibility
- Efficient handling of large datasets
- Reliable forecasting

---

## Repository Structure

```
Devops-CA1/
│── data/                # Raw datasets (holidays_events.csv, oil.csv, stores.csv, test.csv, transactions.csv, sample_submission.csv)
│── feature_engineering.py  # Feature engineering scripts
│── load_data.py            # Data loading utilities
│── preprocess.py           # Data preprocessing scripts
│── train_model.py          # Model training script
│── predict.py              # Prediction script
│── submit.py               # Submission file generator
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
│── submission.csv          # Example submission
```

---

## Data Description

- **holidays_events.csv**: Contains information about holidays and events.
- **oil.csv**: Daily oil price data.
- **stores.csv**: Metadata for each store.
- **test.csv**: Test set for predictions.
- **transactions.csv**: Store transaction counts.
- **sample_submission.csv**: Example format for competition submission.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ady24s/store-sales-forecasting.git
   cd store-sales-forecasting
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Preprocess Data**
   ```bash
   python preprocess.py
   ```
2. **Feature Engineering**
   ```bash
   python feature_engineering.py
   ```
3. **Train Model**
   ```bash
   python train_model.py
   ```
4. **Make Predictions**
   ```bash
   python predict.py
   ```
5. **Generate Submission**
   ```bash
   python submit.py
   ```

---

## Modeling Approach

- Implemented time series forecasting models (e.g., Prophet, XGBoost, LightGBM).
- Performed feature engineering using holiday, oil, and store metadata.
- Evaluated models using standard metrics (e.g., RMSE, MAE).

---

## Results

- Achieved competitive accuracy compared to Kaggle baselines.
- Built a reproducible pipeline with DevOps practices for CI/CD and version control.

---

## DevOps Practices

- Version control with Git and GitHub
- Automated workflows for reproducibility
- Modular code for easy maintenance


---

## Team Members

- **Adyasha Subhadarsini**
- **Trisha Boda**
- **Atharva Gondhali**
- **Aarya Patil**

