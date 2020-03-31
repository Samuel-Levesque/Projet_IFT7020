include "globals.mzn"; 
include "scenario1.dzn";

int: n; % number of players
int: num_courts; % number of courts

int: m = n*(n-1) div 2; % number of matches

% decision variables
array[1..n, 1..n] of var 0..m: x;

var 0..m: z = max(array1d(x)); % max number of match (to minimize)

% predicates

% solve minimize z;
solve :: int_search(array1d(x), most_constrained, indomain_split, complete) minimize z;

constraint


  % upper triangle
  forall(k in 1..n) (
    % sum([x[i,j]=k | i,j in 1..n where i < j]) <= num_courts
    % at_most(num_courts, [x[i,j]=k | i,j in 1..n where i < j], k)
    count(t in [x[i,j]=k | i,j in 1..n where i < j])(t=k) <= num_courts
  )

  /\
  forall(i in 1..n) (
    x[i,i] = 0 /\
    forall(j in 1..n where i != j) (
      x[i,j] > 0 /\
      x[i,j] = x[j,i]
    )
  )
  /\ % a player must rest at least one match after a match
  forall(p in 1..n) (
    forall(p2,p3 in 1..n where p2 != p /\ p3 != p /\ p2 < p3) (
      abs(x[p,p2]-x[p,p3]) >= 2
    )
  )

  /\ % symmetry breaking
     % first player's game are sorted
  increasing([x[1,j]| j in 1..n])

  /\ x[1,2] = 1
;

output 
[
  "n: \(n) num_courts: \(num_courts)\n",
  "z: \(z)\n",
]
++
[ "\n\nMatches:\n"] 
++
[
  if fix(x[p1,p2]) = match then
    "Match " ++ show_int(2,match) ++ ": " ++ show_int(2,p1) ++ " vs " ++ show_int(2,p2) ++ "\n"
  else
   ""
  endif
  | match in 1..fix(z), p1,p2 in 1..n where p1 < p2
]
++
[ "\nMatch grid:\n"]
++
[
  if j = 1 then "\n" else " " endif ++
    show_int(3, x[i,j])
  | i,j in 1..n
]
++
[
 "\nz: \(z)\n"
]
;