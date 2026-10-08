"""Visualization utilities for the tempxplain backend."""

from clingo import Control
from clingo.script import enable_python
from clingraph.clingo_utils import ClingraphContext
from clingraph.graphviz import compute_graphs, render
from clingraph.orm import Factbase

from tempxplain.utils.logging import get_logger
from tempxplain.utils.symbols import to_program

from .api import ServerState
from .explain import MODEL_STRING_FOIL_TYPE, MODEL_STRING_REF_TYPE, Model

DPI = 80


log = get_logger("tempxplain.visualize")


def visualize_domain(state: ServerState, model: MODEL_STRING_REF_TYPE | MODEL_STRING_FOIL_TYPE, t: int) -> str | None:
    """Visualize the domain of the model at time step t with clingraph."""
    if state.program_data.viz_file is None:
        log.warning("No visualization file was provided, so nothing was rendered.")
        return None
    fb = Factbase(prefix="v")
    ctl = Control(["--warn=none", "--const", f"setdpi={DPI}"])
    model_state_t = state.explanation.get_model_state_at(Model(model), t)
    ctl.add("base", [], to_program(model_state_t))
    ctl.load(state.program_data.viz_file)
    enable_python()
    ctl.ground([("base", [])], context=ClingraphContext())
    ctl.solve(on_model=fb.add_model)
    graphs = compute_graphs(fb, graphviz_type="directed")
    files = render(graphs, view=False, directory="out", name_format=f"{model}-{t}", format="svg")
    # TODO : Open file and convert to base64, then return
    if len(files) == 0:
        log.warning("No graph images were rendered.")
        return graphs
    log.info("Graph image saved in: %s", files["explanation"])
    return graphs
