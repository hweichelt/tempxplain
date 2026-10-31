% [1] Removal of assumptions
cost(assumption(R),1,1) :- tag(R, assume(_)), program(R, ref), not program(R, foil).

% [2] Changes to the Instance
cost(instance(R),1,2) :- tag(R, instance), program(R, ref), not program(R, foil).
cost(instance(R),1,2) :- tag(R, instance), not program(R, ref), program(R, foil).

% [3] Other changes (the domain encoding)
cost(encoding(R),1,3) :- not tag(R, instance), not tag(R, assume(_)),
                         program(R, ref), not program(R, foil).
cost(encoding(R),1,3) :- not tag(R, instance),
                         not program(R, ref), program(R, foil).
