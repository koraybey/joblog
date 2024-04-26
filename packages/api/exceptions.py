from markdownify import MarkdownConverter


class UnconfiguredEnvironmentError(Exception):
    """Raise error if any of the required keys in .env is missing."""



class InvalidInputError(Exception):
    """Raise error if DOM element is not found."""

    def __init__(self, el_name: str):
        super().__init__(f"{el_name} not found or tag type is invalid.")
