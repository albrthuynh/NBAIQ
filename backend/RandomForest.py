import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

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

# Define parameter grid for RandomizedSearchCV
param_dist = {
    "n_estimators": [50, 100, 200, 300],
    "max_depth": [5, 10, 15, 20, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "bootstrap": [True, False]
}


# Uncomment below to run hyperparameter search
#search = RandomizedSearchCV(
#     RandomForestClassifier(random_state=42, n_jobs=-1),
#     param_distributions=param_dist,
#     n_iter=20,
#     scoring="accuracy",
#     cv=3,
#     verbose=1,
#     n_jobs=-1
# )
#search.fit(X_train_scaled, y_train)
#print("Best parameters found:", search.best_params_)

# Best parameters found: {'n_estimators': 100, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_depth': 10, 'bootstrap': True}
# Train the Random Forest model
print("Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,  # Number of trees
    max_depth=10,  # Maximum depth of each tree
    min_samples_split=2,  # Minimum samples required to split an internal node
    min_samples_leaf=1,  # Minimum samples required to be at a leaf node
    random_state=42,
    bootstrap=True 
)

model.fit(X_train_scaled, y_train.values.ravel())  # Use ravel to convert y_train to 1D array

# Make predictions
print("Making predictions on the test set...")
y_pred = model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

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

def RandomForestModel(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        bootstrap=True 
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model.fit(X_train_scaled, y_train.values.ravel()) 
    return model, scaler

# Test teams here
if __name__ == "__main__":
    # Example usage:
    compare_teams_across_seasons(
        home_team="Utah Jazz", home_season=2025,
        away_team="Oklahoma City Thunder", away_season=2025,
        scaler=scaler, model=model
    )