export interface Api {
  ping: { params: Record<string, never>; result: "pong" };
  set_program: { params: { program: string }; result: null };
  get_program: { params: Record<string, never>; result: string };
  get_program_data: { params: Record<string, never>; result: ProgramData };
  get_explanation: { params: Record<string, never>; result: Explanation };
  parse_query: {
    params: { query_raw: string };
    result: QueryResult;
  };
  get_visualization: {
    params: { model: Model; t: number };
    result: string | null;
  };
}

export type Model = "ref" | "foil";
export type ModelMembership = "none" | "ref" | "foil" | "both";

export type ProgramData = {
  files: string[];
};

export type Node = {
  type: string;
  id: string;
  models: Model[];
  programs: Model[];
  constraint?: boolean;
  time?: number;
  label?: string;
  title?: string;
  atom_type?: "action" | "fluent";
  first_order?: string;
};

export type Edge = {
  type: "negative" | "positive";
  source: string;
  target: string;
};

export type GraphQuery = {
  query_atom: string;
  type: string;
};

export type Graph = {
  nodes: Node[];
  edges: Edge[];
  query: GraphQuery[];
};

export type Explanation = {
  program: string;
  graph: Graph;
  partitions: Record<number, string[]>;
  timeframe_full: [number, number];
  timeframe_explanation: [number, number];
  fluent_matrix: Record<string, ModelMembership[]>;
};

export type QueryResult = {
  query_raw: string;
  queries: Query[] | null;
  error: QueryError | null;
};

export type QueryError = {
  message: string;
  start: number;
  end: number;
};

export type Query = {
  raw: string;
  tex: string;
  timestep: number | null;
};
