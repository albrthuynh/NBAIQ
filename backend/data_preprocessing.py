import pandas as pd
from sklearn.model_selection import train_test_split

def load_data():
    games_data = pd.read_csv("data/Games.csv", dtype={15: str})
    team_stats_data = pd.read_csv("data/Team Stats Per 100 Poss.csv")
    games_data["season"] = games_data["gameDate"].str[:4].astype(int)

    # Create a mapping from team names to team IDs for all seasons
    team_mapping = {}
    for _, row in team_stats_data.iterrows():
        team_name = row["team"]
        season = row["season"]
        season_games = games_data[games_data["season"] == season]
        team_games = season_games[
            (season_games["hometeamName"] == team_name.split()[-1])
            | (season_games["awayteamName"] == team_name.split()[-1])
        ]
        if not team_games.empty:
            team_id = (
                team_games.iloc[0]["hometeamId"]
                if team_games.iloc[0]["hometeamName"] == team_name.split()[-1]
                else team_games.iloc[0]["awayteamId"]
            )
            team_mapping[(season, team_name)] = team_id

    # Create features for each game
    game_features = []
    game_outcomes = []
    game_meta = []

    for _, game in games_data.iterrows():
        season = game["season"]
        home_team_id = game["hometeamId"]
        away_team_id = game["awayteamId"]
        winner_id = game["winner"]

        home_team_name = None
        away_team_name = None
        for (team_season, team_name), team_id in team_mapping.items():
            if team_season == season:
                if team_id == home_team_id:
                    home_team_name = team_name
                elif team_id == away_team_id:
                    away_team_name = team_name

        if home_team_name and away_team_name:
            home_stats = team_stats_data[
                (team_stats_data["season"] == season) & (team_stats_data["team"] == home_team_name)
            ].iloc[0]
            away_stats = team_stats_data[
                (team_stats_data["season"] == season) & (team_stats_data["team"] == away_team_name)
            ].iloc[0]

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

            outcome = 1 if winner_id == home_team_id else 0

            game_features.append(features)
            game_outcomes.append(outcome)
            game_meta.append({
                "season": season,
                "home_team": home_team_name,
                "away_team": away_team_name
            })

    features_df = pd.DataFrame(game_features)
    outcomes_series = pd.Series(game_outcomes)
    meta_df = pd.DataFrame(game_meta)

    # Save processed data
    print("Data preprocessing complete. Saving processed data...")
    features_df.to_csv("data/processed_features.csv", index=False)
    outcomes_series.to_csv("data/processed_outcomes.csv", index=False)
    meta_df.to_csv("data/processed_meta.csv", index=False)
    print("Processed data saved successfully.")


if __name__ == "__main__":
    # Example usage:
    load_data()