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
