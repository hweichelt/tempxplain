graph(robots).
attr(graph,robots,bgcolor,transparent).

attr(node,N,fontname,"JetBrainsMono"):- node(N,_).


node(cell(POS),robots):- cell(POS).
attr(node,cell(POS),shape,square):- cell(POS).
attr(node,cell(POS),label,""):- cell(POS).
attr(node,cell(POS),width,"1"):- cell(POS).
attr(node,cell((X,Y)),pos,@pos(X,Y)):- cell((X,Y)).
attr(node,cell(POS),penwidth,3):- cell(POS).
attr(node,cell(POS),class,"vs-gray-3"):- cell(POS).

node(robot(R),robots):- at(R,POS).
attr(node,robot(R),label,R):- at(R,POS).
attr(node,robot(R),shape,rectangle):- at(R,POS).
attr(node,robot(R),width,"0.6"):- at(R,POS).
attr(node,robot(R),height,"0.6"):- at(R,POS).
attr(node,robot(R),pos,@pos(X,Y)):- at(R,(X,Y)).
attr(node,robot(R),penwidth,0):- at(R,POS).
attr(node,robot(R),style,"rounded,filled"):- at(R,POS).
attr(node,robot(R),class,"vb-gray-2"):- at(R,POS).
