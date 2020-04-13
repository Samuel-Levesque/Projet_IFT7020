include "globals.mzn"; 
% include "toy.dzn";

int: NB_PERIODS;
int: NB_VENUES;
int: NB_DIVISIONS;
int: NB_TEAMS;
int: NB_GAMES;
enum TEAM_NAMES;
enum COACH_NAMES;

set of int: venues = 1..NB_VENUES;
set of int: periods = 1..NB_PERIODS;
set of int: games = 1..NB_GAMES;
set of int: divisions = 1..NB_DIVISIONS;
set of int: teams = 1..NB_TEAMS;

array[divisions] of int: NB_TEAMS_PER_DIVISION;
array[TEAM_NAMES, periods] of int: TEAMS_TIME_PREFERENCES; % Cost matrix by team/period to minimize
array[games, 1..2] of TEAM_NAMES: GAMES_TO_SCHEDULE;
array[venues, periods] of bool: VENUE_AVAILABILITIES;
array[TEAM_NAMES] of COACH_NAMES: COACHES_BY_TEAM;

% DFA that defines the number of breaks
% - Q number of states. It depends on the # of periods as break
% - S domain of the values 1..S
% - q0 first state
% - STATE set of all the states
% - dfa the transition table
int: S = 2;
% int: Q = 6; int: q0 = 1; set of int: STATE = 1..Q;
% array[STATE,1..2] of int: dfa =
% [|6,2
%  |3,0
%  |4,0
%  |5,0
%  |6,0
%  |6,2|];

%  one period of break
int: Q = 4; int: q0 = 1; set of int: STATE = 1..Q;
array[STATE, 1..2] of int: dfa =
     [|4,2
 |3,0
 |4,0
 |4,2|];

% Decision variables
array[venues, periods] of var 0..NB_GAMES: schedule;
array[TEAM_NAMES, venues, periods] of var bool: team_playing;
array[COACH_NAMES, periods] of var int: coach_playing;
array[TEAM_NAMES, periods] of var int: time_costs;
var int: preferences_cost = sum(time_costs);


% Constraints

% Game is only scheduled when venue is available
constraint forall(v in venues, p in periods) (
    not VENUE_AVAILABILITIES[v, p] -> schedule[v, p] = 0
  );

% Each game is only played once
constraint alldifferent_except_0(schedule);

% The total number of matches played must be equal to the total number of matchs
constraint among(array1d(schedule), games) = NB_GAMES;

% Filling out the team_playing matrix 
constraint forall (t in TEAM_NAMES, v in venues, p in periods) (
    team_playing[t, v, p] <-> (schedule[v, p] > 0) /\ (GAMES_TO_SCHEDULE[schedule[v, p], 1] = t \/ GAMES_TO_SCHEDULE[schedule[v, p], 2] = t)
  );
  
% Making sure a team does not play two games at the same time
constraint forall(t in TEAM_NAMES, p in periods) (
    sum(team_playing[t, venues, p]) <= 1
  );
  
% Filling out time_costs matrix
constraint forall(t in TEAM_NAMES, p in periods) (
    time_costs[t, p] = sum(team_playing[t, venues, p]) * TEAMS_TIME_PREFERENCES[t, p]
  );
  
% Filling out coach_playing matrix
constraint forall(c in COACH_NAMES, p in periods) (
    coach_playing[c, p] = sum(t in TEAM_NAMES where COACHES_BY_TEAM[t] = c, v in venues)(team_playing[t, v, p])
  );
  
% A coach cannot play two matches at the same time
constraint forall(c in COACH_NAMES, p in periods) (coach_playing[c, p] <= 1);

% Forces a minimun number of periods between games
constraint forall(t in TEAM_NAMES) (
    regular([sum(team_playing[t, venues, p])+1 | p in periods], Q, S, dfa, q0, 2..Q) 
  );

% solve
% solve :: int_search([schedule[v,p] | v in venues, p in periods], most_constrained, indomain_split, complete) satisfy;
solve :: int_search(time_costs, smallest, indomain_min, complete) minimize preferences_cost;

output 
["Schedule: \n"]
++
[
  join(" ", [show(schedule[v, p]) | p in periods]) ++ "\n" | v in venues
]
++
[
  join("", [show(sum(team_playing[t, venues, p])) | p in periods]) ++ "\n" | t in TEAM_NAMES
];