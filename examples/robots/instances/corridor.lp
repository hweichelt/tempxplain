#const horizon = 7.

cell((0,0)).              cell((2,0)).
cell((0,1)). cell((1,1)). cell((2,1)).
cell((0,2)).              cell((2,2)).

robot(1). robot(2).

start(1,(0,2)). goal(1,(2,0)).
start(2,(2,2)). goal(2,(0,0)).
