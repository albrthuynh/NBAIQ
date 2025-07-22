import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from nba_data import load_and_prepare_data

# Load the datasets
print("Loading and preparing data...")
X_train, X_test, y_train, y_test, meta_train, meta_test = load_and_prepare_data()
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

# After training, allow user to specify season and team for prediction -----------------------------
target_season = 2024  # Change this to desired season
target_team = "Golden State Warriors"  # Change this to desired team name

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
    print(meta_team_test)


# Function to get team stats for a specific season
def get_team_stats(team_stats_data, team_name, season):
    stats = team_stats_data[(team_stats_data["season"] == season) & (team_stats_data["team"].str.lower() == team_name.lower())]
    if stats.empty:
        raise ValueError(f"Stats not found for {team_name} in {season}")
    return stats.iloc[0]


# Function to build feature vector for a game
def build_feature_vector(home_stats, away_stats):
    # Same feature engineering as in nba_data.py
    features = {
        "fg_pct_diff": home_stats["fg_percent"] - away_stats["fg_percent"],
        "x3p_pct_diff": home_stats["x3p_percent"] - away_stats["x3p_percent"],
        "x2p_pct_diff": home_stats["x2p_percent"] - away_stats["x2p_percent"],
        "ft_pct_diff": home_stats["ft_percent"] - away_stats["ft_percent"],
        "fg_per_100_diff": home_stats["fg_per_100_poss"] - away_stats["fg_per_100_poss"],
        "fga_per_100_diff": home_stats["fga_per_100_poss"] - away_stats["fga_per_100_poss"],
        "x3p_per_100_diff": home_stats["x3p_per_100_poss"] - away_stats["x3p_per_100_poss"],
        "x3pa_per_100_diff": home_stats["x3pa_per_100_poss"] - away_stats["x3pa_per_100_poss"],
        "x2p_per_100_diff": home_stats["x2p_per_100_poss"] - away_stats["x2p_per_100_poss"],
        "x2pa_per_100_diff": home_stats["x2pa_per_100_poss"] - away_stats["x2pa_per_100_poss"],
        "ft_per_100_diff": home_stats["ft_per_100_poss"] - away_stats["ft_per_100_poss"],
        "fta_per_100_diff": home_stats["fta_per_100_poss"] - away_stats["fta_per_100_poss"],
        "orb_per_100_diff": home_stats["orb_per_100_poss"] - away_stats["orb_per_100_poss"],
        "drb_per_100_diff": home_stats["drb_per_100_poss"] - away_stats["drb_per_100_poss"],
        "trb_per_100_diff": home_stats["trb_per_100_poss"] - away_stats["trb_per_100_poss"],
        "ast_per_100_diff": home_stats["ast_per_100_poss"] - away_stats["ast_per_100_poss"],
        "stl_per_100_diff": home_stats["stl_per_100_poss"] - away_stats["stl_per_100_poss"],
        "blk_per_100_diff": home_stats["blk_per_100_poss"] - away_stats["blk_per_100_poss"],
        "tov_per_100_diff": away_stats["tov_per_100_poss"] - home_stats["tov_per_100_poss"],
        "pf_per_100_diff": home_stats["pf_per_100_poss"] - away_stats["pf_per_100_poss"],
        "pts_per_100_diff": home_stats["pts_per_100_poss"] - away_stats["pts_per_100_poss"],
        "efg_pct_diff": (
            (home_stats["fg_per_100_poss"] + 0.5 * home_stats["x3p_per_100_poss"])
            / home_stats["fga_per_100_poss"]
        ) - (
            (away_stats["fg_per_100_poss"] + 0.5 * away_stats["x3p_per_100_poss"])
            / away_stats["fga_per_100_poss"]
        ),
        "pace_diff": (
            home_stats["fga_per_100_poss"]
            + home_stats["fta_per_100_poss"] * 0.44
            + home_stats["tov_per_100_poss"]
        ) - (
            away_stats["fga_per_100_poss"]
            + away_stats["fta_per_100_poss"] * 0.44
            + away_stats["tov_per_100_poss"]
        ),
    }
    return pd.DataFrame([features])

# Function to compare teams across seasons
def compare_teams_across_seasons(home_team, home_season, away_team, away_season, scaler, model):
    # Load team stats data
    team_stats_data = pd.read_csv("data/Team Stats Per 100 Poss.csv")
    # Get stats for both teams
    home_stats = get_team_stats(team_stats_data, home_team, home_season)
    away_stats = get_team_stats(team_stats_data, away_team, away_season)
    # Build feature vector
    features = build_feature_vector(home_stats, away_stats)
    # Scale features
    features_scaled = scaler.transform(features)
    # Predict
    pred = model.predict(features_scaled)[0]
    proba = model.predict_proba(features_scaled)[0]
    winner = home_team if pred == 1 else away_team
    print(f"\n{home_team} ({home_season}) vs {away_team} ({away_season}):")
    print(f"Predicted winner: {winner}")
    print(f"Probability {home_team} wins: {proba[1]:.3f}, {away_team} wins: {proba[0]:.3f}")


# Test teams here
if __name__ == "__main__":
    # Example usage:
    compare_teams_across_seasons(
        home_team="Utah Jazz", home_season=2025,
        away_team="Oklahoma City Thunder", away_season=2025,
        scaler=scaler, model=model
    )