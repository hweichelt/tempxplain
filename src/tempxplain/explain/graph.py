"""Functionality for representing and constructing temporal explanation graphs."""

import re
from dataclasses import dataclass
from functools import cached_property
from typing import cast

from asplain.llm.utils import Graph
from asplain.llm.utils.graph import JsonGraph
from clingo import Symbol

from tempxplain.utils.symbols import to_program

PATTERN_FLUENT = r"holds\((.*),\d+\)"
PATTERN_ACTION = r"occurs\((.*),\d+\)"
LABEL_ATOM_TYPE = "atom_type"
ATOM_TYPE_FLUENT = "fluent"
ATOM_TYPE_ACTION = "action"


@dataclass(frozen=True)
class TemporalExplanationGraph:
    """Represents a temporal explanation graph."""

    graph: Graph

    @classmethod
    def from_symbols(cls, symbols: set[Symbol]) -> "TemporalExplanationGraph":
        """Construct a TemporalExplanationGraph from a set of clingo Symbols."""
        return cls(graph=Graph(to_program(symbols)))

    @cached_property
    def json(self) -> JsonGraph:
        """Return the graph as a JSON-serializable dictionary."""
        return temporal_transform_graph_json(self.graph.json)


def temporal_transform_graph_json(graph: JsonGraph) -> JsonGraph:
    """Transform a default asplain explanation graph JSON to a temporal explanation graph JSON."""
    transformed = graph.copy()

    pattern_fluent = re.compile(PATTERN_FLUENT)
    pattern_action = re.compile(PATTERN_ACTION)
    for i, node in enumerate(graph["nodes"]):
        node_label = cast(str, node["id"])
        if matches := re.search(pattern_fluent, node_label):
            transformed["nodes"][i]["title"] = matches.group(1)
            transformed["nodes"][i][LABEL_ATOM_TYPE] = ATOM_TYPE_FLUENT
            continue
        if matches := re.search(pattern_action, node_label):
            transformed["nodes"][i]["title"] = matches.group(1)
            transformed["nodes"][i][LABEL_ATOM_TYPE] = ATOM_TYPE_ACTION
    return transformed
