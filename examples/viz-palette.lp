graph(palette).
attr(graph,palette,bgcolor,transparent).

attr(node,N,fontname,"JetBrainsMono"):- node(N,_).


color((0,0), "red", "vb-red vt-foreground vs-t").
color((1,0), "purple", "vb-purple vt-foreground vs-t").
color((2,0), "blue", "vb-blue vt-foreground vs-t").
color((3,0), "green", "vb-green vt-foreground vs-t").
color((4,0), "yellow", "vb-yellow vt-foreground vs-t").

color((0,1), "gray-1", "vb-gray-1 vt-foreground vs-t").
color((1,1), "gray-2", "vb-gray-2 vt-foreground vs-t").
color((2,1), "gray-3", "vb-gray-3 vt-foreground vs-t").
color((3,1), "gray-4", "vb-gray-4 vt-foreground vs-t").
color((4,1), "orange", "vb-orange vt-foreground vs-t").


color((0,2), "white", "vb-white vt-black vs-t").
color((1,2), "black", "vb-black vt-white vs-t").
color((2,2), "back\nground", "vb-background vt-foreground vs-t").
color((3,2), "fore\nground", "vb-foreground vt-background vs-t").
color((4,2), "muted", "vb-muted vt-muted-foreground vs-t").


node(cell(POS),palette):- color(POS,_,_).
attr(node,cell(POS),shape,square):- color(POS,_,_).
attr(node,cell(POS),label,L):- color(POS,L,_).
attr(node,cell(POS),width,"0.95"):- color(POS,_,_).
attr(node,cell((X,Y)),pos,@pos(X,Y)):- color((X,Y),_,_).
attr(node,cell(POS),style,"rounded,filled"):- color(POS,_,_).
attr(node,cell(POS),class,C):- color(POS,_,C).
