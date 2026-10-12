import ELK, {
  type ElkExtendedEdge,
  type ElkNode,
} from "elkjs/lib/elk.bundled.js";
import { MarkerType, Position, type Edge, type Node } from "@xyflow/svelte";

import type { GraphData, GraphNode } from "./graph_data";

export type SectionData = { label: string };
export type LayoutResult = { nodes: Node[]; edges: Edge[] };

const NODE_WIDTH = 100;
const NODE_HEIGHT = 40;
const SECTION_LABEL_HEIGHT = 32;
const SECTION_PADDING = 16;
const STATIC_SECTION_ID = "section:static";

const elk = new ELK();

export function section_id(t: number | null): string {
  return t === null ? STATIC_SECTION_ID : `section:${t}`;
}

function section_label(t: number | null): string {
  return t === null ? "static" : `${t}`;
}

/* TODO : Maybe do this in the backend already and pass a complex graph object */
function group_by_timepoint(
  nodes: GraphNode[],
): [number | null, GraphNode[]][] {
  const sections = new Map<number | null, GraphNode[]>();
  for (const node of nodes) {
    sections.set(node.t, [...(sections.get(node.t) ?? []), node]);
  }
  return [...sections.entries()].sort(
    ([a], [b]) => (a ?? -Infinity) - (b ?? -Infinity),
  );
}

function to_elk_graph(data: GraphData): ElkNode {
  const children: ElkNode[] = group_by_timepoint(data.nodes).map(
    ([t, nodes], partition) => ({
      id: section_id(t),
      layoutOptions: {
        "elk.partitioning.partition": String(partition),
        "elk.padding": `[top=${SECTION_LABEL_HEIGHT + SECTION_PADDING},left=${SECTION_PADDING},bottom=${SECTION_PADDING},right=${SECTION_PADDING}]`,
      },
      children: nodes.map((node) => ({
        id: node.id,
        width: NODE_WIDTH,
        height: NODE_HEIGHT,
      })),
    }),
  );
  const edges: ElkExtendedEdge[] = data.edges.map((edge) => ({
    id: edge.id,
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

export async function layout_graph(data: GraphData): Promise<LayoutResult> {
  const labels = new Map(data.nodes.map((node) => [node.id, node.label]));
  const result = await elk.layout(to_elk_graph(data));

  const nodes: Node[] = [];
  for (const section of result.children ?? []) {
    const t =
      section.id === STATIC_SECTION_ID
        ? null
        : Number(section.id.slice("section:".length));
    nodes.push({
      id: section.id,
      type: "section",
      data: { label: section_label(t) } satisfies SectionData,
      position: { x: section.x ?? 0, y: section.y ?? 0 },
      width: section.width,
      height: section.height,
      selectable: false,
      draggable: false,
    });
    for (const child of section.children ?? []) {
      nodes.push({
        id: child.id,
        data: { label: labels.get(child.id) ?? child.id },
        // ELK child coordinates are relative to the parent, just like in SvelteFlow
        position: { x: child.x ?? 0, y: child.y ?? 0 },
        width: child.width,
        height: child.height,
        parentId: section.id,
        extent: "parent",
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
      });
    }
  }

  const edges: Edge[] = data.edges.map((edge) => ({
    ...edge,
    type: "smoothstep",
    markerEnd: { type: MarkerType.ArrowClosed },
  }));

  return { nodes, edges };
}
