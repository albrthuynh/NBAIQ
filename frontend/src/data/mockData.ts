import type { Team, Player } from '../types/index';

export const teams: Team[] = [
  { id: '1', name: 'Lakers', city: 'Los Angeles', logo: '🏀', wins: 47, losses: 35, offensiveRating: 115.2, defensiveRating: 112.8 },
  { id: '2', name: 'Warriors', city: 'Golden State', logo: '🏀', wins: 44, losses: 38, offensiveRating: 117.8, defensiveRating: 115.1 },
  { id: '3', name: 'Celtics', city: 'Boston', logo: '🏀', wins: 57, losses: 25, offensiveRating: 118.2, defensiveRating: 111.3 },
  { id: '4', name: 'Heat', city: 'Miami', logo: '🏀', wins: 44, losses: 38, offensiveRating: 112.9, defensiveRating: 110.7 },
];

export const mvpCandidates: Player[] = [
  { id: '1', name: 'Jayson Tatum', team: 'Boston Celtics', ppg: 30.1, rpg: 8.8, apg: 4.9, mvpProbability: 87 },
  { id: '2', name: 'Giannis Antetokounmpo', team: 'Milwaukee Bucks', ppg: 31.1, rpg: 11.8, apg: 5.7, mvpProbability: 82 },
  { id: '3', name: 'Luka Dončić', team: 'Dallas Mavericks', ppg: 32.4, rpg: 8.6, apg: 8.0, mvpProbability: 78 },
  { id: '4', name: 'Joel Embiid', team: 'Philadelphia 76ers', ppg: 33.1, rpg: 10.2, apg: 4.2, mvpProbability: 75 },
];