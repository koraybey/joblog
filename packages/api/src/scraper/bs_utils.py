import re
from typing import Any
import bs4
from exceptions import InvalidInputError

ElementType = bs4.element.Tag | bs4.element.NavigableString | None

def get_text(el: ElementType, el_name: str) -> str:
    if el and isinstance(el, bs4.element.Tag):
        return el.get_text(strip=True)
    else:
        raise InvalidInputError(el_name)

def get_children(el: ElementType, el_name: str) -> bs4.element.ResultSet:
    if el and isinstance(el, bs4.element.Tag):
        return el.findChildren()
    else:
        raise InvalidInputError(el_name)

def check_el_type(el: ElementType, el_name: str) -> bs4.element.Tag:
    if el and isinstance(el, bs4.element.Tag):
        return el
    else:
        raise InvalidInputError(el_name)

def return_first_match(text: str, regex: str) -> Any | None:
    try:
        result = re.findall(regex, text)[0]
    except (Exception, IndexError):
        result = None
    return result