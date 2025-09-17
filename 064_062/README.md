# Smoker Status Prediction

This project is based on the Kaggle Playground Series S3E24 challenge:  
[Kaggle Challenge](https://www.kaggle.com/competitions/playground-series-s3e24)

## Objective
Build a machine learning model to predict whether a patient is a smoker based on biomedical features.

## Tech Stack
- Python 3.9
- Pandas
- Scikit-learn
- Docker
- GitHub Actions (CI/CD)

## How to Run
1. Download `train.csv` from the Kaggle challenge page and place it in the `data/` folder.
2. Build and run the Docker container:
    ```bash
    docker build -t smoker-prediction .
    docker run smoker-prediction
    ```

## Team Members
- [Gargi Mittal]
- [G Karthick]

## Source
https://www.kaggle.com/competitions/playground-series-s3e24
