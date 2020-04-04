include "globals.mzn"; 
include "scenario2.dzn";

int: NB_PERIODS;
int: NB_VENUES;
int: GAME_DURATION;
int: NB_GAMES;
int: NB_TEAMS;
int: NB_DIVISIONS;

set of int: games = 1..NB_GAMES;
set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;

array[1..NB_DIVISIONS] of int: NB_TEAMS_PER_DIVISION;
array[venues, periods] of bool: VENUE_AVAILABILITIES;
array[1..NB_GAMES, 1..2] of string: GAMES_TO_SCHEDULE;


% decision variables
array[venues, periods] of var 0..NB_GAMES: schedule;
array[games] of var 1..NB_GAMES: scheduled_games;


constraint
  forall(v in venues, p in periods) (
    not VENUE_AVAILABILITIES[v, p] -> schedule[v, p] = 0
  );

constraint  
  among(array1d(schedule), games) = NB_GAMES;
 
 constraint  
  alldifferent_except_0(schedule);
  
 
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
%   "Scheduled:" ++ show(scheduled_games)
% ]
;