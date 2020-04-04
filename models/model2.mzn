include "globals.mzn"; 
include "scenario2.dzn";

int: NB_PERIODS;
int: NB_VENUES;
int: GAME_DURATION;
int: NB_GAMES;
int: NB_TEAMS;
int: NB_DIVISIONS;
enum TEAM_NAMES_ENUM;

set of int: games = 1..NB_GAMES;
set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;
set of int: divisions = 1..NB_DIVISIONS;
set of int: teams = 1..NB_TEAMS;

array[divisions] of int: NB_TEAMS_PER_DIVISION;
array[venues, periods] of bool: VENUE_AVAILABILITIES;
array[games, 1..2] of TEAM_NAMES_ENUM: GAMES_TO_SCHEDULE;
array[teams] of string: TEAM_NAMES;

% decision variables
array[venues, periods] of var 0..NB_GAMES: schedule;
array[TEAM_NAMES_ENUM, periods] of var bool: team_playing;


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
  forall(v in venues, p in periods) (    
      team_playing[GAMES_TO_SCHEDULE[schedule[v,p], 1], p] = (schedule[v,p] > 0)	 /\
      team_playing[GAMES_TO_SCHEDULE[schedule[v,p], 2], p] = (schedule[v,p] > 0)	 /\ 
         
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
++
[
  join(" ", [show(team_playing[t, p]) | p in periods]) ++ "\n" | t in TEAM_NAMES_ENUM
]
++
[
    show(GAMES_TO_SCHEDULE[1, 1])
]
% ++
% [
%   join(" ", [show(GAMES_TO_SCHEDULE[g, o]) | o in 1..2]) ++ "\n" | g in games
% ]

;