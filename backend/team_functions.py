import pandas as pd

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

    return home_team, home_season, proba[1], away_team, away_season, proba[0], winner