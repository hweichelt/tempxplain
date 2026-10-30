% Robots Temporal Example

% @time(T) :: occurs(A,T)
% @time(T) :: holds(F,T)

time(0..horizon).

% Define actions
action_type(up). action_type(down). action_type(left). action_type(right).
% Define fulents
fluent(at). fluent(reached_goal).
% Directional move differences
diff(up,(0,-1)). diff(down,(0,1)). diff(left,(-1,0)). diff(right,(1,0)).
% connected cells
edge((X,Y),(X+DX,Y+DY)) :- cell((X,Y)), cell((X+DX,Y+DY)), diff(A,(DX,DY)).

% ACTION GENERATION

% @label("At time {} action {} occurs",(T,A,))
% @time(T)
{occurs(action(R,A),T): action_type(A)} :- time(T),time(T+1), robot(R).
% @label("At time {} there cannot be two actions {} and {} for the same robot {}.",(T,A1,A2,R,))
% @time(T)
:- time(T), time(T+1), occurs(action(R,A1),T), occurs(action(R,A2),T), A1!=A2.
% explicitly encode that action happens for asplain
has_action(R,T) :- occurs(action(R,A),T).

% ACTION CONDITIONS

% @label("Robot {} cannot move up from ({},{}) at {} since there is no cell there.",(R,X,Y,T,))
% @time(T)
:- occurs(action(R,up),T), holds(at(R,(X,Y)),T), not cell((X,Y-1)).
% @label("Robot {} cannot move down from ({},{}) at {} since there is no cell there.",(R,X,Y,T,))
% @time(T)
:- occurs(action(R,down),T), holds(at(R,(X,Y)),T), not cell((X,Y+1)).
% @label("Robot {} cannot move left from ({},{}) at {} since there is no cell there.",(R,X,Y,T,))
% @time(T)
:- occurs(action(R,left),T), holds(at(R,(X,Y)),T), not cell((X-1,Y)).
% @label("Robot {} cannot move right from ({},{}) at {} since there is no cell there.",(R,X,Y,T,))
% @time(T)
:- occurs(action(R,right),T), holds(at(R,(X,Y)),T), not cell((X+1,Y)).

% INITIAL POSITIONS

holds(at(R,POS),0) :- start(R,POS).

% CAUSAL RULES

% @label("Robot {} moves {} from ({},{}) at time {}",(R,A,X,Y,T,))
% @time(T)
holds(at(R,(X+DX,Y+DY)),T+1) :- occurs(action(R,A),T), diff(A,(DX,DY)), holds(at(R,(X,Y)),T), cell((X+DX,Y+DY)).
% @label("Robot {} reached its goal position {} at time {}",(R,POS,T,))
% @time(T)
holds(reached_goal(R),T) :- holds(at(R,POS),T), goal(R,POS).

% INERTIA RULES

% @label("Robot {} doesn't move from {} at {} since no action is chosen",(R,POS,T,))
% @time(T)
% @inertia
holds(at(R,POS),T+1) :- holds(at(R,POS),T), not has_action(R,T), time(T).
% @label("Robot {} already reached its goal position at {}",(R,T,))
% @time(T)
% @inertia
holds(reached_goal(R),T+1) :- holds(reached_goal(R),T), not has_action(R,T), time(T).

% CONSTRAINTS

% @label("Robot {} has to have reached its goal position at the time horizon {}",(R,T,))
% @time(T)
:- not holds(reached_goal(R),T), robot(R), time(T), not time(T+1).

% @label("Vertex conflict for robots {} and {} at node {} at time {}",(R1,R2,POS,T,))
% @time(T)
:- holds(at(R1,POS),T), holds(at(R2,POS),T), time(T), R1<R2.
% @label("Edge conflict for robots {} and {} at nodes {} and {} at time {}",(R1,R2,POS1,POS2,T,))
% @time(T)
:- holds(at(R1,POS1),T), holds(at(R2,POS2),T), holds(at(R1,POS2),T+1), holds(at(R2,POS1),T+1), edge(POS1,POS2), R1<R2.

#show occurs/2.
