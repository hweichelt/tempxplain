"""Functionality for representing and constructing temporal explanation graphs."""

from dataclasses import dataclass
from functools import cached_property

from asplain.llm.utils import Graph
from asplain.llm.utils.graph import JsonGraph
from clingo import Symbol

from tempxplain.utils.symbols import to_program


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
        return self.graph.json
