import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data():
    features_df = pd.read_csv("data/processed_features.csv")
    outcomes_series = pd.read_csv("data/processed_outcomes.csv")
    meta_df = pd.read_csv("data/processed_meta.csv")

     # Split the data
    X_train, X_test, y_train, y_test, meta_train, meta_test = train_test_split(
        features_df,
        outcomes_series,
        meta_df,
        test_size=0.2,
        random_state=42,
        stratify=outcomes_series,
    )

    # Remove NaN values from both X_train and y_train together
    train_notna = X_train.notna().all(axis=1)
    X_train = X_train[train_notna]
    y_train = y_train[train_notna]

    # Remove NaN values from both X_test and y_test together
    test_notna = X_test.notna().all(axis=1)
    X_test = X_test[test_notna]
    y_test = y_test[test_notna]
    meta_test = meta_test[test_notna]

    # Reset indices after filtering
    X_test = X_test.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)
    meta_test = meta_test.reset_index(drop=True)

    return X_train, X_test, y_train, y_test, meta_train, meta_test

