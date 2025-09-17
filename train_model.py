import xgboost as xgb
from feature_engineering import add_features
from preprocess import preprocess

def train_xgb():
    train, _ = preprocess()
    train = add_features(train)

    # Define features and target
    features = ['store_nbr', 'family', 'type', 'cluster', 'transactions',
                'day', 'month', 'year', 'weekday', 'is_weekend']
    target = 'sales'

    # Clip negative sales to 0
    train[target] = train[target].clip(lower=0)

    X = train[features]
    y = train[target]

    # Train model
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        objective='reg:squarederror',
        tree_method='hist',
        random_state=42
    )
    model.fit(X, y)

    return model

if __name__ == "__main__":
    model = train_xgb()
    print("Model trained.")