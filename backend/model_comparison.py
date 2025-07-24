import pandas as pd

from LogisticRegression import LogisticRegressionModel
from XGBoost import XGBoostModel
from RandomForest import RandomForestModel
from team_functions import compare_teams_across_seasons
from data_testing import prepare_data

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

    for name, (model, scaler) in models.items():
        print()
        print(f"\nUsing {name} model...")
        print(f"Comparing teams: {home_team} ({home_season}) vs {away_team} ({away_season})")
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
        print(f"{name}: Predicted winner: {winner} | {home_team} win prob: {home_prob:.3f}, {away_team} win prob: {away_prob:.3f}")

    print("\n=== Ensemble (Average) Results ===")
    print(f"Average probability {home_team} wins: {avg_home_prob:.3f}")
    print(f"Average probability {away_team} wins: {avg_away_prob:.3f}")
    print(f"Predicted winner: {winner}")


if __name__ == "__main__":
    # Example usage:
    home_team = "Golden State Warriors"
    home_season = 2025
    away_team = "Utah Jazz"
    away_season = 2025
    compare_models(home_team, home_season, away_team, away_season)