export type GraphNode = {
  id: string;
  label: string;
  t: number | null;
};

export type GraphEdge = {
  id: string;
  source: string;
  target: string;
};

export type GraphData = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};

export const example_graph: GraphData = {
  nodes: [
    { id: "floor(1)", label: "floor(1)", t: null },
    { id: "floor(2)", label: "floor(2)", t: null },
    { id: "floor(3)", label: "floor(3)", t: null },
    { id: "floor(4)", label: "floor(4)", t: null },
    { id: "n1", label: "A", t: 0 },
    { id: "n2", label: "B", t: 0 },
    { id: "n3", label: "C", t: 1 },
    { id: "n4", label: "D", t: 2 },
    { id: "n5", label: "E", t: 2 },
  ],
  edges: [
    { id: "e1", source: "floor(1)", target: "n1" },
    { id: "e2", source: "floor(4)", target: "n1" },
    { id: "e3", source: "n1", target: "n2" },
    { id: "e4", source: "n2", target: "n3" },
    { id: "e5", source: "n3", target: "n4" },
    { id: "e6", source: "n4", target: "n5" },
    { id: "e6", source: "n2", target: "n4" },
  ],
};
