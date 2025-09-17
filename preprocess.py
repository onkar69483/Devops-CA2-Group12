import pandas as pd
from load_data import load_all_data

def preprocess():
    train, test, stores, _, transactions, oil, holidays = load_all_data()

    # Convert date columns
    train['date'] = pd.to_datetime(train['date'])
    test['date'] = pd.to_datetime(test['date'])
    oil['date'] = pd.to_datetime(oil['date'])
    holidays['date'] = pd.to_datetime(holidays['date'])
    transactions['date'] = pd.to_datetime(transactions['date'])

    # Merge store info
    train = train.merge(stores, on='store_nbr', how='left')
    test = test.merge(stores, on='store_nbr', how='left')

    # Merge transactions
    train = train.merge(transactions, on=['date', 'store_nbr'], how='left')
    test = test.merge(transactions, on=['date', 'store_nbr'], how='left')

    # Fill missing transactions with 0
    train['transactions'] = train['transactions'].fillna(0)
    test['transactions'] = test['transactions'].fillna(0)

    return train, test

if __name__ == "__main__":
    train, test = preprocess()
    print("Train after preprocessing:", train.shape)
    print("Test after preprocessing:", test.shape)
    print(train.head())