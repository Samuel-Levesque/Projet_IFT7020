include "globals.mzn"; 
include "scenario2.dzn";

int: NB_PERIODS;
int: NB_VENUES;
int: GAME_DURATION;
int: NB_GAMES; % 3*(3-1)/2 + 3*(3-1)/2
int: NB_TEAMS;
int: NB_DIVISIONS;

array[1..NB_DIVISIONS] of int: NB_TEAMS_PER_DIVISION;
array[venues, periods] of bool: VENUE_AVAILABILITIES;
array[1..NB_GAMES, 2] of string: GAMES_TO_SCHEDULE;

set of int: games = 1..NB_GAMES;
set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;


% decision variables
array[venues, periods] of var 1..NB_GAMES: schedule;


constraint

  forall(v in venues, p in periods) (
    schedule[v, p] > 0 <-> VENUE_AVAILABILITIES[v, p]
  );
 
 
% solve
solve :: int_search([schedule[v,p] | v in venues, p in periods], most_constrained, indomain_split, complete) satisfy;

output 
[
  show(schedule)
]
;