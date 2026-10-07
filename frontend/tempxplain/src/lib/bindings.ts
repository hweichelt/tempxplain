export interface Api {
  ping: { params: Record<string, never>; result: "pong" };
  set_program: { params: { program: string }; result: null };
  get_program: { params: Record<string, never>; result: string };
  get_program_data: { params: Record<string, never>; result: ProgramData };
  get_explanation: { params: Record<string, never>; result: Explanation };
}

export type ProgramData = {
  files: string[];
};

export type Explanation = {
  graph: string;
  partitions: Record<number, string[]>;
  timeframe_full: [number, number];
  timeframe_explanation: [number, number];
  fluent_matrix: Record<string, string[]>;
};
