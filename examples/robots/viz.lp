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


% Choose robot background color out of predefined palette
attr(node,robot(0),class,"vb-yellow vt-fg"):- robot(0).
attr(node,robot(1),class,"vb-red vt-fg"):- robot(1).
attr(node,robot(2),class,"vb-blue vt-fg"):- robot(2).
attr(node,robot(3),class,"vb-orange vt-fg"):- robot(3).
attr(node,robot(4),class,"vb-purple vt-fg"):- robot(4).
attr(node,robot(5),class,"vb-green vt-fg"):- robot(5).
attr(node,robot(X),class,"vb-gray-2 vt-fg"):- robot(X), X>5.
