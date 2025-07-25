import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

from team_functions import compare_teams_across_seasons
from data_testing import prepare_data

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

def LogisticRegressionModel(X_train, y_train):
    model = LogisticRegression(
        penalty='l2', 
        C=10.0, 
        solver='saga', 
        max_iter=500, 
        random_state=42,
        n_jobs=-1  
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model.fit(X_train_scaled, y_train.values.ravel())
    return model, scaler

def compare_models(home_team, home_season, away_team, away_season):
    # Load the datasets
    print("Loading and preparing data...")
    X_train, X_test, y_train, y_test, meta_train, meta_test = prepare_data()
    print("Data loaded successfully.")

    # Initialize models
    models = {
        "Logistic Regression": LogisticRegressionModel(X_train=X_train, y_train=y_train),
        "XGBoost": XGBoostModel(X_train=X_train, y_train=y_train),
        "Random Forest": RandomForestModel(X_train=X_train, y_train=y_train)
    }

    home_probs = []
    away_probs = []
    winners = []
    model_predictions = []

    print(f"\nComparing teams: Home: {home_team} ({home_season}) vs Away: {away_team} ({away_season})")
    for name, (model, scaler) in models.items():
        print()
        print(f"\nUsing {name} model...")
        result = compare_teams_across_seasons(
            home_team, home_season, away_team, away_season, scaler=scaler, model=model
        )
        print(result)
        # Unpack result: (home_team, home_season, home_prob, away_team, away_season, away_prob, winner)
        _, _, home_prob, _, _, away_prob, winner = result
        home_probs.append(home_prob)
        away_probs.append(away_prob)
        winners.append(winner)
        model_predictions.append((name, winner, home_prob, away_prob))

    # Calculate average probabilities
    avg_home_prob = sum(home_probs) / len(home_probs)
    avg_away_prob = sum(away_probs) / len(away_probs)
    winner = home_team if avg_home_prob > avg_away_prob else away_team

    print("\n=== Individual Model Predictions ===")
    for name, winner, home_prob, away_prob in model_predictions:
        print(f"\n{name}: Predicted winner: {winner}")
        print(f"Probability {home_team} wins: {home_prob:.3f}, {away_team} wins: {away_prob:.3f}")

    print("\n=== Average Results ===")
    print(f"Average probability {home_team} wins: {avg_home_prob:.3f}")
    print(f"Average probability {away_team} wins: {avg_away_prob:.3f}")
    print(f"\nPredicted winner: {winner}\n")

    return {
        "home_team": home_team,
        "home_season": home_season,
        "away_team": away_team,
        "away_season": away_season,
        "avg_home_prob": avg_home_prob,
        "avg_away_prob": avg_away_prob,
        "predicted_winner": winner
    }


if __name__ == "__main__":
    # Example usage:
    home_team = "Chicago Bulls"
    home_season = 2025
    away_team = "Indiana Pacers"
    away_season = 2025
    results = compare_models(home_team, home_season, away_team, away_season)