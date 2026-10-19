"""
The backend API.

Functions are exposed by decorating them with `@rpc.method()`. Their return value has to be JSON serializable.
"""

from typing import Literal

from tempql.error import ParseError
from tempql.parser import parse
from tempql.utils import to_tex

from ..explain import MODEL_STRING_FOIL_TYPE, MODEL_STRING_REF_TYPE, Explanation, Model, ModelGraph
from ..utils.logging import get_logger
from ..visualize import visualize_domain
from .bindings import ModelFoil, ModelReference, ProgramData, Query, QueryError, QueryResult
from .rpc import Registry
from .server import ServerState

__all__ = ["rpc"]

log = get_logger("tempxplain.api")
rpc: Registry[ServerState] = Registry()


TEX_QUERY_MODEL = "\\mathbf{\\text{Foil}}"


@rpc.method()
def ping(_state: ServerState) -> Literal["pong"]:
    """Check that the backend is online and reachable."""
    return "pong"


@rpc.method()
def get_visualization(state: ServerState, model: MODEL_STRING_REF_TYPE | MODEL_STRING_FOIL_TYPE, t: int) -> str | None:
    """Get the domain visualization of the specified model at time `t` as svg."""
    m = Model(model)
    match m:
        case Model.REFERENCE:
            graph = state.current_reference[1] if state.current_reference else None
        case Model.FOIL:
            graph = state.current_explanation[1].full if state.current_explanation else None
    if graph is None:
        log.warning(f"Cannot generate visualization for model {model} since there is none available")
        return None
    t_start = graph.interval[0]
    t_end = graph.interval[1]
    log.info(f"{t}, [{t_start},{t_end}]")
    if not (t_start <= t <= t_end):
        log.warning(f"Cannot generate visualization at t={t} since it is out of bounds [{t_start},{t_end}]")
        return None
    return visualize_domain(state, graph, m, t)


@rpc.method()
def get_program_data(state: ServerState) -> ProgramData:
    """Get data for the input programs."""
    return state.program_data


@rpc.method()
def set_query(state: ServerState, query: str) -> None:
    """Set the query string."""
    log.info(f"Setting query: {query}")
    state._query = query


@rpc.method()
def get_query(state: ServerState) -> str | None:
    """Get the query string."""
    return state._query


@rpc.method()
def next_foil(state: ServerState) -> ModelFoil | None:
    """Find the next foil model."""
    foil_found = state.next_explanation()
    if foil_found:
        return get_foil(state)
    # Return None if the foil models are exhausted
    return None


@rpc.method()
def get_reference(state: ServerState) -> ModelReference | None:
    """Get the reference model."""
    match state.current_reference:
        case None:
            return None
        case (ref_id, ref):
            return ModelReference(
                id=ref_id,
                program=ref.program,
                partitions={t: [str(a.symbol) for a in atoms] for t, atoms in ref.partitions.items()},
                timeframe_full=ref.interval,
                fluent_matrix={str(f): [m.value for m in membership] for f, membership in ref.fluent_matrix.items()},
            )


@rpc.method()
def get_foil(state: ServerState) -> ModelFoil | None:
    """Get details of the logic program."""
    match state.current_explanation:
        case None:
            return None
        case ((ref_id, foil_id), exp):
            return ModelFoil(
                id=foil_id,
                reference_id=ref_id,
                program=exp.transformed.program,
                graph=exp.graph.json,
                partitions={t: [str(a.symbol) for a in atoms] for t, atoms in exp.transformed.partitions.items()},
                timeframe_full=exp.full.interval,
                timeframe_explanation=exp.transformed.interval,
                fluent_matrix={
                    str(f): [m.value for m in membership] for f, membership in exp.transformed.fluent_matrix.items()
                },
            )


@rpc.method()
def parse_query(state: ServerState, query_raw: str) -> QueryResult:
    """Get data for the input programs."""
    log.debug(f"Parsing query: {query_raw}")
    try:
        queries = parse(query_raw)
        return QueryResult(
            query_raw, [Query("RAW", to_tex(q, model=TEX_QUERY_MODEL), q.timestep) for q in queries], None
        )
    except ParseError as e:
        error = QueryError(e.message, e.start, e.end)
        return QueryResult(query_raw, None, error)
