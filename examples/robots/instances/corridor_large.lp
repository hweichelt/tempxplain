#const horizon=17.

cell((0..2,0..6)). cell((3,3)). cell((4..6,0..6)).

robot(0). robot(1). robot(2). robot(3).

start(0,(0,0)). goal(0,(6,6)).
start(1,(6,6)). goal(1,(0,0)).
start(2,(0,6)). goal(2,(6,0)).
start(3,(6,0)). goal(3,(0,6)).
