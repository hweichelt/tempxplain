#const horizon=4.

cell((0,0)). cell((1,0)). cell((2,0)).
cell((0,1)). cell((1,1)). cell((2,1)).
cell((0,2)). cell((1,2)). cell((2,2)).

robot(0). robot(1).

start(0, (0,0)). goal(0, (2,2)).
start(1, (2,2)). goal(1, (0,0)).
