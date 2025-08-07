import pandas as pd
from preprocess import preprocess

def add_features(df):
    # Date-based features
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['weekday'] = df['date'].dt.weekday
    df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)

    # Encode store type and family as categorical
    df['type'] = df['type'].astype('category').cat.codes
    df['family'] = df['family'].astype('category').cat.codes

    return df

if __name__ == "__main__":
    train, test = preprocess()
    train = add_features(train)
    test = add_features(test)

    print(train[['date', 'store_nbr', 'family', 'type', 'transactions', 'weekday', 'is_weekend']].head())