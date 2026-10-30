"""Exceptions raised by tempxplain."""


class VisualizationError(Exception):
    """
    Raised when visualization fails.
    """

    def __init__(self, message: str) -> None:
        """Initialize the error with a message."""
        self.message = message
        super().__init__(self.message)
