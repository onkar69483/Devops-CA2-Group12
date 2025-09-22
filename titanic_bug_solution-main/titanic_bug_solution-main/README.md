# titanic_bug_solution

This project is based on the [Kaggle Titanic: Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic) competition.  
The goal is to predict which passengers survived the Titanic disaster using passenger data such as age, sex, ticket class, and fare.

The notebook (`notebook.ipynb`) contains the full workflow — from data loading and preprocessing to model training, prediction, and submission file generation.

---

## 📂 Project Structure
├── notebook.ipynb # Jupyter Notebook with complete analysis and model building
├── train.csv # Training dataset (from Kaggle)
├── test.csv # Test dataset (from Kaggle)
├── gender_submission.csv # Example submission file from Kaggle
├── requirements.txt # Python dependencies
└── README.md


---

## 📊 Dataset

From Kaggle competition page:
- **train.csv** → Passenger data with survival outcome (`Survived` column)
- **test.csv** → Passenger data without survival outcome (predictions needed)
- **gender_submission.csv** → Example of correct submission format

**Features:**
- PassengerId
- Pclass (ticket class)
- Name
- Sex
- Age
- SibSp (siblings/spouses aboard)
- Parch (parents/children aboard)
- Ticket
- Fare
- Cabin
- Embarked (port of embarkation)

---

## 🧠 Workflow in Notebook

1. **Import Libraries**
2. **Load Data** (`train.csv`, `test.csv`)
3. **Data Exploration** — summary stats, missing values, survival rates
4. **Feature Engineering** — handling missing values, encoding categorical variables, creating new features
5. **Model Training** — using machine learning algorithms (e.g., Logistic Regression, Random Forest, etc.)
6. **Model Evaluation** — accuracy on validation set
7. **Generate Predictions** for `test.csv`
8. **Create Submission File** in the required Kaggle format

---

## ⚙️ Installation

```bash
pip install -r requirements.txt



