import ELK, {
  type ElkExtendedEdge,
  type ElkNode,
} from "elkjs/lib/elk.bundled.js";
import { MarkerType, Position, type Edge, type Node } from "@xyflow/svelte";

import type { Graph, Node as BackendNode } from "$lib/bindings";

export type SectionData = { label: string };
export type LayoutResult = { nodes: Node[]; edges: Edge[] };

const NODE_ATOM_WIDTH = 100;
const NODE_ATOM_HEIGHT = 40;
const NODE_RULE_WIDTH = 40;
const NODE_RULE_HEIGHT = 40;
const node_type_dimensions = new Map([
  ["rule(disjunction)", [NODE_RULE_WIDTH, NODE_RULE_HEIGHT]],
  ["rule(choice)", [NODE_RULE_WIDTH, NODE_RULE_HEIGHT]],
  ["atom", [NODE_ATOM_WIDTH, NODE_ATOM_HEIGHT]],
]);
const DEFAULT_NODE_WIDTH = NODE_ATOM_WIDTH;
const DEFAULT_NODE_HEIGHT = NODE_ATOM_HEIGHT;

const SECTION_LABEL_HEIGHT = 32;
const SECTION_PADDING = 16;
const SECTION_ID_PREFIX = "section:";

const node_type_labels = new Map([
  ["rule(disjunction)", "rule_disjunction"],
  ["rule(choice)", "rule_choice"],
  ["atom", "atom"],
]);
const DEFAULT_NODE_TYPE = "default";

const elk = new ELK();

export function edge_id(source: string, target: string): string {
  return [source, target].join("-");
}

export function section_id(t: number): string {
  return `${SECTION_ID_PREFIX}${t}`;
}

function group_by_timepoint(
  nodes: BackendNode[],
): [number | null, BackendNode[]][] {
  const sections = new Map<number | null, BackendNode[]>();
  for (const node of nodes) {
    sections.set(node.time ?? null, [
      ...(sections.get(node.time ?? null) ?? []),
      node,
    ]);
  }
  return [...sections.entries()].sort(
    ([a], [b]) => (a ?? -Infinity) - (b ?? -Infinity),
  );
}

function to_elk_node(node: BackendNode): ElkNode {
  return {
    id: node.id,
    width: node_type_dimensions.get(node.type)?.[0] ?? DEFAULT_NODE_WIDTH,
    height: node_type_dimensions.get(node.type)?.[1] ?? DEFAULT_NODE_HEIGHT,
  };
}

function to_elk_graph(data: Graph): ElkNode {
  const children: ElkNode[] = [];
  let partition = 0;
  for (const [t, nodes] of group_by_timepoint(data.nodes)) {
    const elk_nodes = nodes.map(to_elk_node);
    if (t === null) {
      children.push(...elk_nodes);
      continue;
    }
    children.push({
      id: section_id(t),
      layoutOptions: {
        "elk.partitioning.partition": String(partition++),
        "elk.padding": `[top=${SECTION_LABEL_HEIGHT + SECTION_PADDING},left=${SECTION_PADDING},bottom=${SECTION_PADDING},right=${SECTION_PADDING}]`,
      },
      children: elk_nodes,
    });
  }

  const edges: ElkExtendedEdge[] = data.edges.map((edge) => ({
    id: edge_id(edge.source, edge.target),
    sources: [edge.source],
    targets: [edge.target],
  }));

  return {
    id: "root",
    layoutOptions: {
      "elk.algorithm": "layered",
      "elk.direction": "RIGHT",
      "elk.hierarchyHandling": "INCLUDE_CHILDREN", // layout in one pass (cross section edges work here)
      "elk.partitioning.activate": "true", // order sections by partition
      "elk.layered.spacing.nodeNodeBetweenLayers": "48",
      "elk.spacing.nodeNode": "24",
      "elk.spacing.componentComponent": "24",
    },
    children,
    edges,
  };
}

function free_node(
  node_data: Map<string, BackendNode>,
  child: ElkNode,
  parent?: ElkNode,
): Node {
  const properties = node_data.get(child.id);
  return {
    id: child.id,
    type: node_type_labels.get(properties?.type ?? "") ?? DEFAULT_NODE_TYPE,
    data: {
      label: properties?.title ?? child.id,
      properties,
    },
    position: { x: child.x ?? 0, y: child.y ?? 0 },
    width: child.width,
    height: child.height,
    ...(parent ? { parentId: parent.id, extent: "parent" as const } : {}),
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  };
}

function is_inertia_edge(
  node_data: Map<string, BackendNode>,
  source_id: string,
  target_id: string,
): boolean {
  // Source node is inertia rule
  if (node_data.get(source_id)?.inertia ?? false) {
    return node_data.get(target_id)?.atom_type === "fluent";
  }
  // Target node is inertia rule
  if (node_data.get(target_id)?.inertia ?? false) {
    return node_data.get(source_id)?.atom_type === "fluent";
  }
}

export async function layout_graph(data: Graph): Promise<LayoutResult> {
  const node_data = new Map(data.nodes.map((node) => [node.id, node]));
  const result = await elk.layout(to_elk_graph(data));

  const nodes: Node[] = [];
  for (const child of result.children ?? []) {
    if (node_data.has(child.id)) {
      nodes.push(free_node(node_data, child));
      continue;
    }
    const t = Number(child.id.slice(SECTION_ID_PREFIX.length));
    nodes.push({
      id: child.id,
      type: "section",
      data: { label: `${t}` } satisfies SectionData,
      position: { x: child.x ?? 0, y: child.y ?? 0 },
      width: child.width,
      height: child.height,
      selectable: false,
      draggable: false,
    });
    for (const grandchild of child.children ?? []) {
      nodes.push(free_node(node_data, grandchild, child));
    }
  }

  const edges: Edge[] = data.edges.map((edge) => ({
    id: edge_id(edge.source, edge.target),
    source: edge.source,
    target: edge.target,
    animated: is_inertia_edge(node_data, edge.source, edge.target),
    markerEnd: { type: MarkerType.ArrowClosed },
  }));

  return { nodes, edges };
}
