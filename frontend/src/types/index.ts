export interface Team {
  id: string;
  name: string;
  city: string;
  logo: string;
  wins: number;
  losses: number;
  offensiveRating: number;
  defensiveRating: number;
}

export interface Player {
  id: string;
  name: string;
  team: string;
  ppg: number;
  rpg: number;
  apg: number;
  mvpProbability: number;
}