from train_model import train_xgb
from feature_engineering import add_features
from preprocess import preprocess

def predict():
    _, test = preprocess()
    test = add_features(test)

    features = ['store_nbr', 'family', 'type', 'cluster', 'transactions',
                'day', 'month', 'year', 'weekday', 'is_weekend']

    model = train_xgb()
    test['sales'] = model.predict(test[features]).clip(0)

    return test[['id', 'sales']]

if __name__ == "__main__":
    predictions = predict()
    print(predictions.head())