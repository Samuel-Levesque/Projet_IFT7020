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
enum TEAM_NAMES;
enum COACH_NAMES;

array[divisions] of int: NB_TEAMS_PER_DIVISION;

% Preferences
array[TEAM_NAMES, periods] of int: TEAMS_TIME_PREFERENCES; % Cost matrix by team/period to minimize

array[games, 1..2] of TEAM_NAMES: GAMES_TO_SCHEDULE;
array[venues, periods] of bool: VENUE_AVAILABILITIES;

array[TEAM_NAMES] of COACH_NAMES: COACHES_BY_TEAM;

% Ensembles
set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;
set of int: games = 1..NB_GAMES;
set of int: divisions = 1..NB_DIVISIONS;
set of int: teams = 1..NB_TEAMS;

% Variables
array[venues, periods] of var 0..NB_GAMES: schedule;
array[TEAM_NAMES, venues, periods] of var bool: team_playing;
%array[games, games] of var bool: restricted_teams; % Matrice d'équipes qui ne peuvent pas jouer contre. Peut être fourni en input.

% Coaches matrix
array[COACH_NAMES, periods] of var int: coach_playing;

% Preferences costs
array[TEAM_NAMES, periods] of var int: time_costs;
var int: preferences_cost = sum(time_costs);

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
constraint forall (t in TEAM_NAMES, v in venues, p in periods) (
  team_playing[t, v, p] <-> (schedule[v, p] > 0) /\ (GAMES_TO_SCHEDULE[schedule[v, p], 1] = t \/ GAMES_TO_SCHEDULE[schedule[v, p], 2] = t)
  );
  
% Making sure a team does not play two games at the same time
constraint forall(t in TEAM_NAMES, p in periods) (
  sum(team_playing[t, venues, p]) <= 1
  );
  
% Filling out time_costs matrix
constraint forall(t in TEAM_NAMES, p in periods)(
  time_costs[t, p] = sum(team_playing[t, venues, p]) * TEAMS_TIME_PREFERENCES[t, p]
  );
  
% Filling out coach_playing matrix
constraint forall(c in COACH_NAMES, p in periods)(
  coach_playing[c, p] = sum(t in TEAM_NAMES where COACHES_BY_TEAM[t] = c, v in venues)(team_playing[t, v, p])
  );
  
% A coach cannot play two matches at the same time
constraint forall(c in COACH_NAMES, p in periods)(coach_playing[c, p] <= 1);

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
[join(" ", [show(team_playing[TEAM_NAMES[6], v, p]) | p in periods]) ++ "\n" | v in venues]
++
[
  "Time Preferences: \n"
]
++
[join(" ", [show(time_costs[i, j]) | j in periods]) ++ "\n" | i in TEAM_NAMES]
++
[
  "Total cost: \n"
]
++
[show(preferences_cost)]
++
[
  "\nCoach Playing: \n"
]
++
[join(" ", [show(coach_playing[i, j]) | j in periods]) ++ "\n" | i in COACH_NAMES];

% Solve
solve minimize preferences_cost;
