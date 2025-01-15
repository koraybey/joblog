
from exceptions import AddBlanklineAfterStrong

def md(html, **options):  # type: ignore[no-untyped-def]
    return AddBlanklineAfterStrong(**options).convert(html)