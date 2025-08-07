import pandas as pd

def load_all_data():
    path = "data/"
    train = pd.read_csv(path + "train.csv")
    test = pd.read_csv(path + "test.csv")
    stores = pd.read_csv(path + "stores.csv")
    items = pd.DataFrame() 
    transactions = pd.read_csv(path + "transactions.csv")
    oil = pd.read_csv(path + "oil.csv")
    holidays = pd.read_csv(path + "holidays_events.csv")

    print("Train:", train.shape)
    print("Test:", test.shape)
    print("Stores:", stores.shape)
    print("Transactions:", transactions.shape)
    print("Oil:", oil.shape)
    print("Holidays:", holidays.shape)

    return train, test, stores, items, transactions, oil, holidays

if __name__ == "__main__":
    load_all_data()