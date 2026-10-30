% Elevator Temporal Example

time(0..horizon).

% Define actions
action(up).
action(down).
action(serve).
% Define fulents
fluent(at).
fluent(serve).
fluent(served).
fluent(called).
fluent(ready).

% ACTION GENERATION

% @label("At time {} action {} occurss",(T,A,))
{occurs(A,T): action(A)} :- time(T),time(T+1).
% @label("At time {} there cannot be two actions {} and {} at the same time.",(T,A1,A2,))
:- time(T), time(T+1), occurs(A1,T), occurs(A2,T), A1!=A2.

% ACTION CONDITIONS

% @label("The elevator cannot move up at time {} since it is already at the top floor {}",(T,X,))
:- occurs(up,T),   holds(at(X),T), not floor(X+1).
% @label("The elevator cannot down up at time {} since it is already at the bottom floor {}",(T,X,))
:- occurs(down,T), holds(at(X),T), not floor(X-1).

% CAUSAL RULES

% @label("The elevator moves from floor {} up at time {} since action up is chosen",(X,T,))
holds(at(X+1),T+1) :- occurs(up,T),   holds(at(X),T).
% @label("The elevator moves from floor {} down at time {} since action down is chosen",(X,T,))
holds(at(X-1),T+1) :- occurs(down,T), holds(at(X),T).
% @label("Serve floor {} at time {} when serve action occurss on floor {}",(X,T,X))
holds(served(X),T) :- holds(at(X),T), occurs(serve,T).
% Compute ready
% @label("The elevator is ready at time {} if at that time is was called to floor {} and also is at that floor",(T,X,))
holds(ready,T) :- holds(called(X),T), holds(at(X),T).

% INERTIA RULES

% @label("The elevator doesn't change its floor at time {} since action wait is chosen",(T,))
holds(at(X),T+1) :- holds(at(X),T), not occurs(up,T), not occurs(down,T), time(T).
% @label("Call elevator for floor {} at {} if elevator was called before and not served",(X,T+1,))
holds(called(X),T+1) :- holds(called(X),T), not holds(served(X),T), time(T).

% CONSTRAINTS

% Only allow calling the elevator inside horizon
% @label("The elevator cannot be called at time {}, because it is outside the allowed timesteps",(T,))
:- holds(called(X),T), not time(T).
