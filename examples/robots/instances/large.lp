#const horizon=17.

cell((0..10,0..7)).

robot(0). robot(1). robot(2). robot(3).

start(0, ( 0,0)). goal(0, (10,7)).
start(1, (10,7)). goal(1, ( 0,0)).
start(2, ( 0,7)). goal(2, (10,0)).
start(3, (10,0)). goal(3, ( 0,7)).
