
% Tag all temporal atoms as timed
tag(atom(A),time(T)) :- symbol_literal(holds(_,T),A).
tag(atom(A),time(T)) :- symbol_literal(occurs(_,T),A).

% Identify head and body time of rules that contain timed atoms
body_time(rule(H,normal(B)),T)      :- rule(H,normal(B)),  literal_tuple(B,ID), tag(atom(|ID|),time(T)).
head_time(rule(disjunction(H),B),T) :- rule(disjunction(H),B), atom_tuple(H,A), tag(atom(A),time(T)).
head_time(rule(choice(H),B),T)      :- rule(choice(H),B),      atom_tuple(H,A), tag(atom(A),time(T)).

% Select time steps to include in minimization. Prefere body times over head times
rule_time(R,T) :- body_time(R,T).
rule_time(R,T) :- head_time(R,T), not body_time(R,_).

% Select minimal rule time as time label
tag(R,time(T_MIN)) :- rule_time(R,_), T_MIN = #min{T: rule_time(R,T)}.
