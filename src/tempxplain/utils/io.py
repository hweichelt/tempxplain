"""I/O utilities for tempxplain."""

from pathlib import Path


def read_file(path: Path) -> str:
    """Read the contents of a file."""
    if path.exists():
        if not path.is_file():
            raise OSError(f"{path} is not a file")
    else:
        raise OSError(f"File {path} does not exist")
    with open(path, "r") as f:
        return f.read()
