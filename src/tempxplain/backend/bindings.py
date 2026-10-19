"""Binding dataclasses for the API."""

from dataclasses import dataclass

from asplain.llm.utils.graph import JsonGraph


@dataclass
class Explanation:
    """Details of the logic program."""

    program: str
    graph: JsonGraph
    partitions: dict[int, list[str]]
    timeframe_full: tuple[int, int]
    timeframe_explanation: tuple[int, int]
    fluent_matrix: dict[str, list[str]]


@dataclass
class ProgramData:
    """Data of the input logic programs."""

    files: list[str]
    viz_file: str | None = None


@dataclass
class Query:
    """Parsed query from the input query string."""

    raw: str
    tex: str
    timestep: int | None


@dataclass
class QueryError:
    """Error parsing the input query."""

    message: str
    start: int
    end: int


@dataclass
class QueryResult:
    """Result of parsing a query."""

    raw: str
    queries: list[Query] | None
    error: QueryError | None


@dataclass
class ModelReference:
    """A reference model of the explanation."""

    id: int
    atoms: list[str]
    fluent_matrix: dict[str, list[str]]


@dataclass
class ModelFoil:
    """A foil model of the explanation."""

    id: int
    reference_id: int
    atoms: list[str]
    fluent_matrix: dict[str, list[str]]
    explanation: Explanation
