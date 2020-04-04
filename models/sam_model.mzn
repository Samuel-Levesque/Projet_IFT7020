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
enum TEAM_NAMES_ENUM;

array[divisions] of int: NB_TEAMS_PER_DIVISION;
array[teams] of string: TEAM_NAMES;


array[games, 1..2] of TEAM_NAMES_ENUM: GAMES_TO_SCHEDULE;
array[venues, periods] of bool: VENUE_AVAILABILITIES;

% Ensembles
set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;
set of int: games = 1..NB_GAMES;
set of int: divisions = 1..NB_DIVISIONS;
set of int: teams = 1..NB_TEAMS;

% Variables
array[venues, periods] of var 0..NB_GAMES: schedule;
array[TEAM_NAMES_ENUM, venues, periods] of var bool: team_playing;
array[games, games] of var bool: restricted_teams; % Matrice d'équipes qui ne peuvent pas jouer contre. Peut être fourni en input.

% Constraints

% Each team cannot play two games at the same time
%constraint forall(i in teams, j in periods)(sum(team_playing[i, venues, j] <= 1));
% Game is only scheduled when venue is available
constraint forall(i in venues, j in periods)(not VENUE_AVAILABILITIES[i, j] -> schedule[i, j]=0);

% Each game is only played once
constraint alldifferent_except_0(schedule);

% The total number of matches played is ok
constraint among(NB_GAMES, array1d(schedule), games);

% Filling out the team_playing matrix
constraint forall (t in TEAM_NAMES_ENUM, v in venues, p in periods) (
  team_playing[t, v, p] <-> (schedule[v, p] > 0) /\ (GAMES_TO_SCHEDULE[schedule[v, p], 1] = t \/ GAMES_TO_SCHEDULE[schedule[v, p], 2] = t)
  );
  
% Making sure a team does not play two games at the same time
constraint forall(t in TEAM_NAMES_ENUM, p in periods) (
  sum(team_playing[t, venues, p]) <= 1
  );

% Output
output 
[
  "Schedule: \n"
]
++
[join(" ", [show(schedule[i, j]) | j in periods]) ++ "\n" | i in venues]
++
[
  "Teams Playing: \n"
]
++
% team_playing;
% [join(" ", [show(team_playing[TEAM_NAMES_ENUM[1], v, p]) | p in periods]) ++ "\n" | v in venues]
% ++
% [join(" ", [show(team_playing[TEAM_NAMES_ENUM[2], v, p]) | p in periods]) ++ "\n" | v in venues]
% ++
% [join(" ", [show(team_playing[TEAM_NAMES_ENUM[3], v, p]) | p in periods]) ++ "\n" | v in venues]
% ++
% [join(" ", [show(team_playing[TEAM_NAMES_ENUM[4], v, p]) | p in periods]) ++ "\n" | v in venues]
% ++ 
% [join(" ", [show(team_playing[TEAM_NAMES_ENUM[5], v, p]) | p in periods]) ++ "\n" | v in venues]
% ++
[join(" ", [show(team_playing[TEAM_NAMES_ENUM[6], v, p]) | p in periods]) ++ "\n" | v in venues];

% Solve
solve satisfy;
