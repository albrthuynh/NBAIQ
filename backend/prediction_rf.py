import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Load the datasets
print("Loading datasets...")
games_data = pd.read_csv("data/Games.csv")
team_stats_data = pd.read_csv("data/Team Stats Per 100 Poss.csv")

# Filter for only the 2025 season
games_2025 = games_data[games_data["gameDate"].str.contains("2025")].copy()
team_stats_2025 = team_stats_data[team_stats_data["season"] == 2025].copy()

# How many games found in the 2025 season
print(f"Found {len(games_2025)} games from 2025 season")
# How many teams found in the 2025 season
print(f"Found {len(team_stats_2025)} team stats records from 2025 season")

# Create a mapping from team names to team IDs
# Each team has their own unqiue ID in the dataset "Games.csv"
team_mapping = {}
for _, row in team_stats_2025.iterrows():
    team_name = row["team"]
    # Extract team ID from games data
    team_games = games_2025[
        (games_2025["hometeamName"] == team_name.split()[-1])
        | (games_2025["awayteamName"] == team_name.split()[-1])
    ]
    if not team_games.empty:
        # Get the team ID (either home or away)
        team_id = (
            team_games.iloc[0]["hometeamId"]
            if team_games.iloc[0]["hometeamName"] == team_name.split()[-1]
            else team_games.iloc[0]["awayteamId"]
        )
        team_mapping[team_name] = team_id

print(f"Created mapping for {len(team_mapping)} teams")

# Create features for each game with more comprehensive stats
game_features = []
game_outcomes = []

for _, game in games_2025.iterrows():
    home_team_id = game["hometeamId"]
    away_team_id = game["awayteamId"]
    winner_id = game["winner"]

    # Find team stats for home and away teams
    home_team_name = None
    away_team_name = None

    # Find team names by matching team IDs
    for team_name, team_id in team_mapping.items():
        if team_id == home_team_id:
            home_team_name = team_name
        elif team_id == away_team_id:
            away_team_name = team_name

    if home_team_name and away_team_name:
        # Get team stats
        home_stats = team_stats_2025[team_stats_2025["team"] == home_team_name].iloc[0]
        away_stats = team_stats_2025[team_stats_2025["team"] == away_team_name].iloc[0]

        # Create comprehensive features comparing team stats
        features = {
            # Shooting efficiency
            "fg_pct_diff": home_stats["fg_percent"] - away_stats["fg_percent"],
            "x3p_pct_diff": home_stats["x3p_percent"] - away_stats["x3p_percent"],
            "x2p_pct_diff": home_stats["x2p_percent"] - away_stats["x2p_percent"],
            "ft_pct_diff": home_stats["ft_percent"] - away_stats["ft_percent"],
            # Volume stats
            "fg_per_100_diff": home_stats["fg_per_100_poss"]
            - away_stats["fg_per_100_poss"],
            "fga_per_100_diff": home_stats["fga_per_100_poss"]
            - away_stats["fga_per_100_poss"],
            "x3p_per_100_diff": home_stats["x3p_per_100_poss"]
            - away_stats["x3p_per_100_poss"],
            "x3pa_per_100_diff": home_stats["x3pa_per_100_poss"]
            - away_stats["x3pa_per_100_poss"],
            "x2p_per_100_diff": home_stats["x2p_per_100_poss"]
            - away_stats["x2p_per_100_poss"],
            "x2pa_per_100_diff": home_stats["x2pa_per_100_poss"]
            - away_stats["x2pa_per_100_poss"],
            "ft_per_100_diff": home_stats["ft_per_100_poss"]
            - away_stats["ft_per_100_poss"],
            "fta_per_100_diff": home_stats["fta_per_100_poss"]
            - away_stats["fta_per_100_poss"],
            # Rebounding
            "orb_per_100_diff": home_stats["orb_per_100_poss"]
            - away_stats["orb_per_100_poss"],
            "drb_per_100_diff": home_stats["drb_per_100_poss"]
            - away_stats["drb_per_100_poss"],
            "trb_per_100_diff": home_stats["trb_per_100_poss"]
            - away_stats["trb_per_100_poss"],
            # Playmaking and defense
            "ast_per_100_diff": home_stats["ast_per_100_poss"]
            - away_stats["ast_per_100_poss"],
            "stl_per_100_diff": home_stats["stl_per_100_poss"]
            - away_stats["stl_per_100_poss"],
            "blk_per_100_diff": home_stats["blk_per_100_poss"]
            - away_stats["blk_per_100_poss"],
            "tov_per_100_diff": away_stats["tov_per_100_poss"]
            - home_stats["tov_per_100_poss"],  # Lower TOV is better
            "pf_per_100_diff": home_stats["pf_per_100_poss"]
            - away_stats["pf_per_100_poss"],
            # Scoring
            "pts_per_100_diff": home_stats["pts_per_100_poss"]
            - away_stats["pts_per_100_poss"],
            # Efficiency ratios
            "efg_pct_diff": (
                (home_stats["fg_per_100_poss"] + 0.5 * home_stats["x3p_per_100_poss"])
                / home_stats["fga_per_100_poss"]
            )
            - (
                (away_stats["fg_per_100_poss"] + 0.5 * away_stats["x3p_per_100_poss"])
                / away_stats["fga_per_100_poss"]
            ),
            # Pace indicators
            "pace_diff": (
                home_stats["fga_per_100_poss"]
                + home_stats["fta_per_100_poss"] * 0.44
                + home_stats["tov_per_100_poss"]
            )
            - (
                away_stats["fga_per_100_poss"]
                + away_stats["fta_per_100_poss"] * 0.44
                + away_stats["tov_per_100_poss"]
            ),
        }

        # Outcome: 1 if home team won, 0 if away team won
        outcome = 1 if winner_id == home_team_id else 0

        game_features.append(features)
        game_outcomes.append(outcome)

print(f"Created {len(game_features)} training samples")

# Convert to DataFrame
features_df = pd.DataFrame(game_features)
outcomes_series = pd.Series(game_outcomes)

print(f"Features shape: {features_df.shape}")
print(f"Outcomes distribution: {outcomes_series.value_counts()}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    features_df,
    outcomes_series,
    test_size=0.2,
    random_state=42,
    stratify=outcomes_series,
)

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Scale the features to prevent overfitting
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model with regularization to prevent overfitting
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    random_state=42,
    min_samples_split=5,
    min_samples_leaf=3,
    class_weight='balanced',
    n_jobs=-1
)

print("Training RandomForest model...")
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.3f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Away Win", "Home Win"]))

# Feature importance
importance = model.feature_importances_
print("\nTop 10 Feature Importance:")
feature_importance = list(zip(features_df.columns, importance))
feature_importance.sort(key=lambda x: x[1], reverse=True)
for i, (feature, imp) in enumerate(feature_importance[:10]):
    print(f"{i+1}. {feature}: {imp:.4f}")

# Test prediction for a specific matchup
print("\n" + "=" * 50)
print("PREDICTION FOR SPECIFIC MATCHUP")
print("=" * 50)

# Let's predict Indiana Pacers vs Oklahoma City Thunder
team1 = "Indiana Pacers"
team2 = "Oklahoma City Thunder"

# Get team stats
team1_stats = team_stats_2025[team_stats_2025["team"] == team1].iloc[0]
team2_stats = team_stats_2025[team_stats_2025["team"] == team2].iloc[0]

# Create features (assuming team1 is home, team2 is away)
prediction_features = {
    "fg_pct_diff": team1_stats["fg_percent"] - team2_stats["fg_percent"],
    "x3p_pct_diff": team1_stats["x3p_percent"] - team2_stats["x3p_percent"],
    "x2p_pct_diff": team1_stats["x2p_percent"] - team2_stats["x2p_percent"],
    "ft_pct_diff": team1_stats["ft_percent"] - team2_stats["ft_percent"],
    "fg_per_100_diff": team1_stats["fg_per_100_poss"] - team2_stats["fg_per_100_poss"],
    "fga_per_100_diff": team1_stats["fga_per_100_poss"]
    - team2_stats["fga_per_100_poss"],
    "x3p_per_100_diff": team1_stats["x3p_per_100_poss"]
    - team2_stats["x3p_per_100_poss"],
    "x3pa_per_100_diff": team1_stats["x3pa_per_100_poss"]
    - team2_stats["x3pa_per_100_poss"],
    "x2p_per_100_diff": team1_stats["x2p_per_100_poss"]
    - team2_stats["x2p_per_100_poss"],
    "x2pa_per_100_diff": team1_stats["x2pa_per_100_poss"]
    - team2_stats["x2pa_per_100_poss"],
    "ft_per_100_diff": team1_stats["ft_per_100_poss"] - team2_stats["ft_per_100_poss"],
    "fta_per_100_diff": team1_stats["fta_per_100_poss"]
    - team2_stats["fta_per_100_poss"],
    "orb_per_100_diff": team1_stats["orb_per_100_poss"]
    - team2_stats["orb_per_100_poss"],
    "drb_per_100_diff": team1_stats["drb_per_100_poss"]
    - team2_stats["drb_per_100_poss"],
    "trb_per_100_diff": team1_stats["trb_per_100_poss"]
    - team2_stats["trb_per_100_poss"],
    "ast_per_100_diff": team1_stats["ast_per_100_poss"]
    - team2_stats["ast_per_100_poss"],
    "stl_per_100_diff": team1_stats["stl_per_100_poss"]
    - team2_stats["stl_per_100_poss"],
    "blk_per_100_diff": team1_stats["blk_per_100_poss"]
    - team2_stats["blk_per_100_poss"],
    "tov_per_100_diff": team2_stats["tov_per_100_poss"]
    - team1_stats["tov_per_100_poss"],
    "pf_per_100_diff": team1_stats["pf_per_100_poss"] - team2_stats["pf_per_100_poss"],
    "pts_per_100_diff": team1_stats["pts_per_100_poss"]
    - team2_stats["pts_per_100_poss"],
    "efg_pct_diff": (
        (team1_stats["fg_per_100_poss"] + 0.5 * team1_stats["x3p_per_100_poss"])
        / team1_stats["fga_per_100_poss"]
    )
    - (
        (team2_stats["fg_per_100_poss"] + 0.5 * team2_stats["x3p_per_100_poss"])
        / team2_stats["fga_per_100_poss"]
    ),
    "pace_diff": (
        team1_stats["fga_per_100_poss"]
        + team1_stats["fta_per_100_poss"] * 0.44
        + team1_stats["tov_per_100_poss"]
    )
    - (
        team2_stats["fga_per_100_poss"]
        + team2_stats["fta_per_100_poss"] * 0.44
        + team2_stats["tov_per_100_poss"]
    ),
}

# Scale the prediction features
prediction_df = pd.DataFrame([prediction_features])
prediction_df_scaled = scaler.transform(prediction_df)

# Make prediction
prediction = model.predict(prediction_df_scaled)[0]
probability = model.predict_proba(prediction_df_scaled)[0]

print(f"\nPrediction for {team1} (Home) vs {team2} (Away):")
print(f"Winner: {team1 if prediction == 1 else team2}")
print(f"Home Win Probability: {probability[1]:.3f}")
print(f"Away Win Probability: {probability[0]:.3f}")

# Show team stats comparison
print(f"\nTeam Stats Comparison:")
print(f"{team1} (Home):")
for stat in [
    "fg_percent",
    "x3p_percent",
    "ft_percent",
    "trb_per_100_poss",
    "ast_per_100_poss",
    "pts_per_100_poss",
]:
    print(f"  {stat}: {team1_stats[stat]:.3f}")
print(f"\n{team2} (Away):")
for stat in [
    "fg_percent",
    "x3p_percent",
    "ft_percent",
    "trb_per_100_poss",
    "ast_per_100_poss",
    "pts_per_100_poss",
]:
    print(f"  {stat}: {team2_stats[stat]:.3f}")

# Test multiple matchups to show more realistic probabilities
print(f"\n" + "=" * 50)
print("MULTIPLE MATCHUP PREDICTIONS")
print("=" * 50)

test_matchups = [
    ("Washington Wizards", "Portland Trail Blazers"),
    ("Portland Trail Blazers", "Washington Wizards"),
    ("Oklahoma City Thunder", "Indiana Pacers"),
    ("Indiana Pacers", "Oklahoma City Thunder"),
    ("Washington Wizards", "Oklahoma City Thunder"),
    ("Oklahoma City Thunder", "Washington Wizards"),
]

for home_team, away_team in test_matchups:
    try:
        home_stats = team_stats_2025[team_stats_2025["team"] == home_team].iloc[0]
        away_stats = team_stats_2025[team_stats_2025["team"] == away_team].iloc[0]

        # Create features
        matchup_features = {
            "fg_pct_diff": home_stats["fg_percent"] - away_stats["fg_percent"],
            "x3p_pct_diff": home_stats["x3p_percent"] - away_stats["x3p_percent"],
            "x2p_pct_diff": home_stats["x2p_percent"] - away_stats["x2p_percent"],
            "ft_pct_diff": home_stats["ft_percent"] - away_stats["ft_percent"],
            "fg_per_100_diff": home_stats["fg_per_100_poss"]
            - away_stats["fg_per_100_poss"],
            "fga_per_100_diff": home_stats["fga_per_100_poss"]
            - away_stats["fga_per_100_poss"],
            "x3p_per_100_diff": home_stats["x3p_per_100_poss"]
            - away_stats["x3p_per_100_poss"],
            "x3pa_per_100_diff": home_stats["x3pa_per_100_poss"]
            - away_stats["x3pa_per_100_poss"],
            "x2p_per_100_diff": home_stats["x2p_per_100_poss"]
            - away_stats["x2p_per_100_poss"],
            "x2pa_per_100_diff": home_stats["x2pa_per_100_poss"]
            - away_stats["x2pa_per_100_poss"],
            "ft_per_100_diff": home_stats["ft_per_100_poss"]
            - away_stats["ft_per_100_poss"],
            "fta_per_100_diff": home_stats["fta_per_100_poss"]
            - away_stats["fta_per_100_poss"],
            "orb_per_100_diff": home_stats["orb_per_100_poss"]
            - away_stats["orb_per_100_poss"],
            "drb_per_100_diff": home_stats["drb_per_100_poss"]
            - away_stats["drb_per_100_poss"],
            "trb_per_100_diff": home_stats["trb_per_100_poss"]
            - away_stats["trb_per_100_poss"],
            "ast_per_100_diff": home_stats["ast_per_100_poss"]
            - away_stats["ast_per_100_poss"],
            "stl_per_100_diff": home_stats["stl_per_100_poss"]
            - away_stats["stl_per_100_poss"],
            "blk_per_100_diff": home_stats["blk_per_100_poss"]
            - away_stats["blk_per_100_poss"],
            "tov_per_100_diff": away_stats["tov_per_100_poss"]
            - home_stats["tov_per_100_poss"],
            "pf_per_100_diff": home_stats["pf_per_100_poss"]
            - away_stats["pf_per_100_poss"],
            "pts_per_100_diff": home_stats["pts_per_100_poss"]
            - away_stats["pts_per_100_poss"],
            "efg_pct_diff": (
                (home_stats["fg_per_100_poss"] + 0.5 * home_stats["x3p_per_100_poss"])
                / home_stats["fga_per_100_poss"]
            )
            - (
                (away_stats["fg_per_100_poss"] + 0.5 * away_stats["x3p_per_100_poss"])
                / away_stats["fga_per_100_poss"]
            ),
            "pace_diff": (
                home_stats["fga_per_100_poss"]
                + home_stats["fta_per_100_poss"] * 0.44
                + home_stats["tov_per_100_poss"]
            )
            - (
                away_stats["fga_per_100_poss"]
                + away_stats["fta_per_100_poss"] * 0.44
                + away_stats["tov_per_100_poss"]
            ),
        }

        # Scale and predict
        matchup_df = pd.DataFrame([matchup_features])
        matchup_df_scaled = scaler.transform(matchup_df)
        pred = model.predict(matchup_df_scaled)[0]
        prob = model.predict_proba(matchup_df_scaled)[0]

        print(f"\n{home_team} (Home) vs {away_team} (Away):")
        print(f"  Winner: {home_team if pred == 1 else away_team}")
        print(f"  Home Win: {prob[1]:.1%}, Away Win: {prob[0]:.1%}")

    except IndexError:
        print(f"\n{home_team} vs {away_team}: Team not found in 2025 data")

