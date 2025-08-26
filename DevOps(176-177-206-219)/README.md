# DevOps - CA 1 Kaggle Classification Challenge
# Spaceship Titanic - Kaggle Classification Challenge

### By:

- Samidha Manjrekar (22070122176)
- Samruddhi Borhade (22070122177)
- Shruti Bist (22070122206)
- Srishti Parulekar (22070122219)

Predict which passengers were transported to an alternate dimension during the mysterious accident on the **Spaceship Titanic**. This project is based on a Kaggle competition and is a binary classification task.

---

## Files Overview

| File | Description |
|------|-------------|
| `train.csv` | Personal records of ~8700 passengers with known `Transported` status |
| `test.csv` | Data for ~4300 passengers without `Transported` labels (prediction required) |
| `sample_submission.csv` | Submission template format |
| `submission.csv` | Your model's predictions ready for submission |
| `spaceship_titanic.ipynb` | Main notebook containing the data processing and model training pipeline |

---

## Problem Statement

Your task is to predict whether a passenger was **`Transported`** to another dimension based on their travel data and personal attributes.

This is a **binary classification** problem:  
- `Transported = True`: The passenger disappeared  
- `Transported = False`: The passenger remained in this dimension

---

## Features

| Column | Description |
|--------|-------------|
| `PassengerId` | Unique ID, grouped by family/travel group |
| `HomePlanet` | Planet passenger came from |
| `CryoSleep` | Whether passenger was in suspended animation |
| `Cabin` | Format `Deck/Number/Side` |
| `Destination` | Destination planet |
| `Age` | Passenger age |
| `VIP` | Paid for special VIP service |
| `RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck` | Expenses at luxury services |
| `Name` | Passenger name |
| `Transported` | **Target** column (True/False) |

---

## Approach

### Data Preprocessing
- Parsed `Cabin` into `Deck`, `CabinNum`, and `Side`
- Handled missing values (mode/median/zero imputation)
- Created features like:
  - `TotalSpend`: Combined luxury expenses
  - `IsAlone`: Whether passenger was traveling alone
  - `Group`: Extracted from `PassengerId`
- Encoded categorical variables with `LabelEncoder`

### Model
- `RandomForestClassifier` from `scikit-learn`
- Used `train_test_split` for validation
- Achieved solid baseline accuracy

---

## Validation

- Split training data 80/20
- Measured **accuracy score** on validation set

---

## Results

```plaintext
Validation Accuracy: ~0.79 (baseline)