import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from data_testing import prepare_data
from team_functions import compare_teams_across_seasons

# Load the datasets
print("Loading and preparing data...")
X_train, X_test, y_train, y_test, meta_train, meta_test = prepare_data()
print("Data loaded successfully.")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

'''
from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    "n_estimators": [100, 200, 300],
    "max_depth": [3, 5, 7, 9],
    "learning_rate": [0.01, 0.05, 0.1, 0.2],
    "subsample": [0.6, 0.8, 1.0],
    "colsample_bytree": [0.6, 0.8, 1.0],
    "reg_alpha": [0, 0.5, 1, 2],
    "reg_lambda": [0.5, 1, 2, 3],
    "min_child_weight": [1, 3, 5]
}

search = RandomizedSearchCV(
    XGBClassifier(objective="binary:logistic", eval_metric="logloss", random_state=42),
    param_distributions=param_dist,
    n_iter=20,
    scoring="accuracy",
    cv=3,
    verbose=1,
    n_jobs=-1
)
search.fit(X_train_scaled, y_train)
print("Best parameters:", search.best_params_) '''

# Best parameters: {'subsample': 0.8, 'reg_lambda': 2, 'reg_alpha': 0, 'n_estimators': 300, 'min_child_weight': 5, 'max_depth': 3, 'learning_rate': 0.05, 'colsample_bytree': 0.8}
print("Training XGBoost model...")
# Train the model with the best parameters
model = XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_estimators=300,  # Fewer trees
    max_depth=3,  # Shallow trees
    learning_rate=0.05,  # Lower learning rate
    reg_alpha=0,  # L1 regularization
    reg_lambda=2,  # L2 regularization
    subsample=0.8,  # Use 80% of samples per tree
    colsample_bytree=0.8,  # Use 80% of features per tree
    min_child_weight=5,  # Require more samples per leaf
)

print("Training model with regularization...")
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.3f}")

# This is for testing purposes
target_season = 2024  # Change this to desired season
target_team = "Golden State Warriors"  # Change this to desired team name
print(f"\nTesting predictions for {target_team} in season {target_season}...")

# Clean team names in meta_test
meta_test["home_team"] = meta_test["home_team"].str.strip().str.lower()
meta_test["away_team"] = meta_test["away_team"].str.strip().str.lower()
target_team_cleaned = target_team.strip().lower()

# Filter test set for games involving the target team and season
mask = (
    (meta_test["season"] == target_season) &
    ((meta_test["home_team"] == target_team_cleaned) | (meta_test["away_team"] == target_team_cleaned))
)

if not mask.any():
    print(f"No test games found for team '{target_team}' in season {target_season}")
else:
    X_team_test = X_test_scaled[mask]
    y_team_test = y_test[mask]
    meta_team_test = meta_test[mask]

    y_pred_team = model.predict(X_team_test)
    accuracy_team = accuracy_score(y_team_test, y_pred_team)
    print(f"\nPrediction accuracy for {target_team} in {target_season}: {accuracy_team:.3f}")
    print(classification_report(y_team_test, y_pred_team))


def XGBoostModel(X_train, y_train):
    model = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_estimators=300,
        max_depth=3,
        learning_rate=0.05,
        reg_alpha=0,
        reg_lambda=2,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=5, 
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model.fit(X_train_scaled, y_train)
    return model, scaler

# Test teams here
if __name__ == "__main__":
    # Example usage:
    compare_teams_across_seasons(
        home_team="Utah Jazz", home_season=2025,
        away_team="Oklahoma City Thunder", away_season=2025,
        scaler=scaler, model=model
    )