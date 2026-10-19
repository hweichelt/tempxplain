"""Visualization utilities for the tempxplain backend."""

import re

from clingo import Control
from clingraph.clingo_utils import ClingraphContext
from clingraph.graphviz import compute_graphs
from clingraph.orm import Factbase
from graphviz import Digraph

from tempxplain.utils.logging import get_logger
from tempxplain.utils.symbols import to_program

from .backend.server import ServerState
from .explain import Model, ModelGraph

__all__ = ["visualize_domain"]

ENGINE = "neato"
FORMAT = "svg"
SVG_PREAMBLE = re.compile(r"^.*?(?=<svg)", re.DOTALL)

log = get_logger("tempxplain.visualize")


def visualize_domain(state: ServerState, graph: ModelGraph, model: Model, t: int, save: bool = True) -> str | None:
    """
    Visualize the domain of the model at time step `t` with clingraph.
    """
    if state.program_data.viz_file is None:
        log.warning("No visualization file was provided, so nothing was rendered.")
        return None
    ctl = Control(["1", "--warn=none"])  # limit to 1 model (no warnings)
    ctl.add("base", [], to_program(graph.get_model_state_at(model, t)))
    ctl.load(state.program_data.viz_file)
    ctl.ground([("base", [])], context=ClingraphContext())
    fb = Factbase()
    ctl.solve(on_model=fb.add_model)

    graphs: dict[str, Digraph] = compute_graphs(fb, graphviz_type="directed")
    # Get first (and only) graph
    name, g = next(iter(graphs.items()))
    log.debug(f"Rendering graph '{name}' for model {model.value} at t={t}")
    svg = g.pipe(format=FORMAT, engine=ENGINE)
    if save:
        log.debug(f"Saving graph '{name}' for model {model.value} at t={t}")
        with open(f"out/{model.value}-{t}.{FORMAT}", "wb") as f:
            f.write(svg)
    return SVG_PREAMBLE.sub("", svg.decode("utf-8"), count=1)
