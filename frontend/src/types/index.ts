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

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (firstName: string, lastName: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}