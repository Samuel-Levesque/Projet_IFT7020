include "globals.mzn";
include "alldifferent.mzn";
include "scenario2.dzn";

% Constantes
int: NB_PERIODS;
int: NB_VENUES;
int: GAME_DURATION;
int: NB_DIVISIONS;
int: NB_TEAMS;
int: NB_GAMES;
array[divisions] of int: NB_TEAMS_PER_DIVISION;
array[teams] of string: TEAM_NAMES;

array[games, 1..2] of string: GAMES_TO_SCHEDULE;
array[venues, periods] of bool: VENUE_AVAILABILITIES;

% Ensembles
set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;
set of int: games = 1..NB_GAMES;
set of int: divisions = 1..NB_DIVISIONS;
set of int: teams = 1..NB_TEAMS;

% Variables
array[venues, periods] of var 0..NB_GAMES: final_schedule;
array[teams, venues, periods] of var bool: team_playing;
array[games, games] of var bool: restricted_teams; % Matrice d'équipes qui ne peuvent pas jouer contre. Peut être fourni en input.

% Constraints

% Each team cannot play two games at the same time
%constraint forall(i in teams, j in periods)(sum(team_playing[i, venues, j] <= 1));
% Game is only scheduled when venue is available
constraint forall(i in venues, j in periods)(not VENUE_AVAILABILITIES[i, j] -> final_schedule[i, j]=0);

% Each game is only played once
constraint alldifferent_except_0(final_schedule);

% The total number of matches played is ok
constraint among(NB_GAMES, array1d(final_schedule), games);

% Output
output 
[
  "Schedule: \n"
]
++
[join(" ", [show(final_schedule[i, j]) | j in periods]) ++ "\n" | i in venues]
++
[
  "Teams Playing: \n"
]
++
[join(" ", [show(team_playing[1, v, p]) | p in periods]) ++ "\n" | v in venues];

% Solve
solve satisfy;
