import { type Node } from "$lib/bindings";

export type NodeData = { label: string; properties: Node };

export interface NodeProps {
  data: NodeData;
  selected: boolean;
}
