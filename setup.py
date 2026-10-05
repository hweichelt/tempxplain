"""
Build the frontend as part of the Python package build.

This is necessary to always serve the current frontend without needing node.
Also necessary for including the frontend in the built package.
"""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

PROJECT_ROOT = Path(__file__).parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "tempxplain"
FRONTEND_OUT = PROJECT_ROOT / "src" / "tempxplain" / "frontend"

log = logging.getLogger("tempxplain.setup")


def build_frontend() -> None:
    """
    Build the frontend with npm.

    If the frontend source dir has no `package.json` check if the frontend was already built and oly fail if both are
    not available.
    """
    if not (FRONTEND_SRC / "package.json").is_file():
        if not (FRONTEND_OUT / "index.html").is_file():
            raise RuntimeError(f"neither frontend sources in '{FRONTEND_SRC}' nor a built frontend in '{FRONTEND_OUT}'")
        return
    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError("npm is required for building the frontend, install Node.js or run 'npm run build' manually")
    if not (FRONTEND_SRC / "node_modules").is_dir():
        log.info("installing frontend dependencies")
        subprocess.run([npm, "ci"], cwd=FRONTEND_SRC, check=True)
    log.info("building frontend")
    subprocess.run([npm, "run", "build"], cwd=FRONTEND_SRC, check=True)


class BuildPy(build_py):
    """Build the frontend before the Python package."""

    def run(self) -> None:
        """Run the command."""
        build_frontend()
        super().run()


class Sdist(sdist):
    """Build the frontend before the source distribution."""

    def run(self) -> None:
        """Run the command."""
        build_frontend()
        super().run()


cmdclass: dict[str, Any] = {"build_py": BuildPy, "sdist": Sdist}
setup(cmdclass=cmdclass)
