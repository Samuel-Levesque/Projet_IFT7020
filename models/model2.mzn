include "globals.mzn"; 
include "scenario2.dzn";

int: NB_PERIODS;
int: NB_VENUES;
int: GAME_DURATION;
int: NB_GAMES;
int: NB_TEAMS;
int: NB_DIVISIONS;
enum TEAM_NAMES;

set of int: games = 1..NB_GAMES;
set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;
set of int: divisions = 1..NB_DIVISIONS;
set of int: teams = 1..NB_TEAMS;

array[divisions] of int: NB_TEAMS_PER_DIVISION;
array[venues, periods] of bool: VENUE_AVAILABILITIES;
array[games, 1..2] of TEAM_NAMES: GAMES_TO_SCHEDULE;

% decision variables
array[venues, periods] of var 0..NB_GAMES: schedule;
array[TEAM_NAMES, venues, periods] of var bool: team_playing;


% constraints
constraint
  forall(v in venues, p in periods) (
    not VENUE_AVAILABILITIES[v, p] -> schedule[v, p] = 0
  );

constraint  
  among(array1d(schedule), games) = NB_GAMES;
 
constraint  
  alldifferent_except_0(schedule);
  
constraint 
  forall (t in TEAM_NAMES, v in venues, p in periods) (
    team_playing[t, v, p] <-> (schedule[v, p] > 0) /\ (GAMES_TO_SCHEDULE[schedule[v, p], 1] = t \/ GAMES_TO_SCHEDULE[schedule[v, p], 2] = t)
  );
  

% Making sure a team does not play two games at the same time
constraint forall(t in TEAM_NAMES, p in periods) (
  sum(team_playing[t, venues, p]) <= 1
  );
 
% solve
solve :: int_search([schedule[v,p] | v in venues, p in periods], most_constrained, indomain_split, complete) satisfy;

output 
[
  "Schedule: \n"
]
++
[
  join(" ", [show(schedule[v, p]) | p in periods]) ++ "\n" | v in venues
]
% ++
% [
%   join(" ", [show(team_playing[t, p]) | p in periods]) ++ "\n" | t in TEAM_NAMES
% ]
++
[
    show(GAMES_TO_SCHEDULE[1, 1])
]
% ++
% [
%   join(" ", [show(GAMES_TO_SCHEDULE[g, o]) | o in 1..2]) ++ "\n" | g in games
% ]

;