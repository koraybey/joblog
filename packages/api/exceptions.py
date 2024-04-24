from markdownify import MarkdownConverter


class UnconfiguredEnvironmentError(Exception):
    """Raise error if any of the required keys in .env is missing."""


# Markdown conversion helper functions.
class AddBlanklineAfterStrong(MarkdownConverter):  # type: ignore[no-any-unimported]
    """Custom MarkdownConverter that adds a blank line after <strong> tag."""

    def convert_strong(self, el, text, convert_as_inline):  # type: ignore[no-untyped-def]
        return super().convert_strong(el, text, convert_as_inline) + "\n\n"


class InvalidInputError(Exception):
    """Raise error if DOM element is not found."""

    def __init__(self, el_name: str):
        super().__init__(f"{el_name} not found or tag type is invalid.")
