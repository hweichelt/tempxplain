"""Binding dataclasses for the API."""

from dataclasses import dataclass


@dataclass
class Explanation:
    """Details of the logic program."""

    graph: str
    partitions: dict[int, list[str]]
    timeframe_full: tuple[int, int]
    timeframe_explanation: tuple[int, int]
    fluent_matrix: dict[str, list[str]]


@dataclass
class ProgramData:
    """Data of the input logic programs."""

    files: list[str]
    viz_file: str | None = None
