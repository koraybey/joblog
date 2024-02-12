import json
import re
import sys
from pathlib import Path
from typing import Any, Literal, LiteralString

import bs4
import torch
import yaml
from bs4 import BeautifulSoup
from jsonref import replace_refs
from markdownify import MarkdownConverter
from PyPDF2 import PdfReader

from models import LinkedInJobPost
from paths import CONFIG_FOLDER

# START
# Utility functions for converting Pydantic models to llama.cpp grammar.
SPACE_RULE = '" "?'

PRIMITIVE_RULES = {
    "boolean": '("true" | "false") space',
    "number": '("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)? space',
    "integer": '("-"? ([0-9] | [1-9] [0-9]*)) space',
    "string": r""" "\"" (
        [^"\\] |
        "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])
      )* "\"" space """,
    "null": '"null" space',
}

INVALID_RULE_CHARS_RE = re.compile(r"[^a-zA-Z0-9-]+")
GRAMMAR_LITERAL_ESCAPE_RE = re.compile(r'[\r\n"]')
GRAMMAR_LITERAL_ESCAPES = {"\r": "\\r", "\n": "\\n", '"': '\\"'}


class SchemaConverter:
    def __init__(self, prop_order: dict):
        # Get rid of the internal states.
        self._prop_order = prop_order
        self._rules = {"space": SPACE_RULE}

    def _format_literal(self, literal: str) -> str:
        escaped = GRAMMAR_LITERAL_ESCAPE_RE.sub(
            lambda m: GRAMMAR_LITERAL_ESCAPES.get(m.group(0)),  # type: ignore[arg-type, return-value]
            json.dumps(literal),
        )
        return f'"{escaped}"'

    def _add_rule(self, name: str, rule: str) -> str:
        esc_name = INVALID_RULE_CHARS_RE.sub("-", name)
        if esc_name not in self._rules or self._rules[esc_name] == rule:
            key = esc_name
        else:
            i = 0
            while f"{esc_name}{i}" in self._rules:
                i += 1
            key = f"{esc_name}{i}"
        self._rules[key] = rule
        return key

    def visit(self, schema: dict, name: str) -> str:
        schema_type = schema.get("type")
        rule_name = name or "root"

        if "oneOf" in schema or "anyOf" in schema:
            rule = " | ".join(
                (
                    self.visit(alt_schema, f'{name}{"-" if name else ""}{i}')
                    for i, alt_schema in enumerate(schema.get("oneOf") or schema["anyOf"])
                )
            )
            return self._add_rule(rule_name, rule)

        elif "const" in schema:
            return self._add_rule(rule_name, self._format_literal(schema["const"]))

        elif "enum" in schema:
            rule = " | ".join(self._format_literal(v) for v in schema["enum"])
            return self._add_rule(rule_name, rule)

        elif schema_type == "object" and "properties" in schema:
            # TODO: `required` keyword
            prop_order = self._prop_order
            prop_pairs = sorted(
                schema["properties"].items(),
                # sort by position in prop_order (if specified) then by key
                key=lambda kv: (prop_order.get(kv[0], len(prop_order)), kv[0]),
            )

            rule = '"{" space'
            for i, (prop_name, prop_schema) in enumerate(prop_pairs):
                prop_rule_name = self.visit(prop_schema, f'{name}{"-" if name else ""}{prop_name}')
                if i > 0:
                    rule += ' "," space'
                rule += rf' {self._format_literal(prop_name)} space ":" space {prop_rule_name}'
            rule += ' "}" space'

            return self._add_rule(rule_name, rule)

        elif schema_type == "array" and "items" in schema:
            # TODO `prefixItems` keyword
            item_rule_name = self.visit(schema["items"], f'{name}{"-" if name else ""}item')
            rule = f'"[" space ({item_rule_name} ("," space {item_rule_name})*)? "]" space'
            return self._add_rule(rule_name, rule)

        else:
            assert schema_type in PRIMITIVE_RULES, f"Unrecognized schema: {schema}"
            return self._add_rule(
                "root" if rule_name == "root" else schema_type,
                PRIMITIVE_RULES[schema_type],
            )

    def format_grammar(self) -> str:
        return "\n".join((f"{name} ::= {rule}" for name, rule in self._rules.items()))


def json_schema_to_grammar(json: dict, prop_order: dict | None = None) -> str:
    prop_order = {name: idx for idx, name in enumerate(prop_order)} if prop_order is not None else {}
    # We don't like internal state and mutations, schema converter needs revisiting
    converter = SchemaConverter(prop_order)
    converter.visit(json, "")
    print(converter.format_grammar())
    return converter.format_grammar()


def json_schema_with_inlining(model: type[Any]) -> dict:
    json_schema = model.model_json_schema()
    replaced = replace_refs(json_schema, proxies=False)
    if "$defs" in replaced:
        del replaced["$defs"]
    print(replaced)
    return replaced  # type: ignore[no-any-return]


# END
# Utility functions for converting Pydantic models to llama.cpp grammar.


def scrape_job_posting(html: dict) -> str:
    soup = BeautifulSoup(html["html"], "html.parser")
    for s in soup.find_all(["script", "form"]):
        s.extract()
    text = soup.get_text(" ", strip=True)
    return text


# START
# Scrape LinkedIn Job Post via Chrome extension.
# Constants for regex patterns
IMAGE_CLASS = "EntityPhoto"
TITLE_CLASS = "job-title"
DESCRIPTION_CLASS = "jobs-description-content__text"
LOCATION_CLASS = "card__bullet"
COMPANY_URL_CLASS = "primary-description-without-tagline"
HIGHLIGHT_INSIGHT_CLASS = "__job-insight--highlight"
SUBTITLE_CLASS = "primary-description-without-tagline"
ERROR_DESCRIPTION = "No matching tag found or is a NavigableString"

# Markdown conversion helper functions.
class AddBlanklineAfterStrong(MarkdownConverter): # type: ignore[no-any-unimported]
    """Custom MarkdownConverter that adds a blank line after <strong> tag."""

    def convert_strong(self, el, text, convert_as_inline): # type: ignore[no-untyped-def]
        return super().convert_strong(el, text, convert_as_inline) + "\n\n"

def md(html, **options): # type: ignore[no-untyped-def]
    return AddBlanklineAfterStrong(**options).convert(html)


def scrape_from_linkedin(html: dict) -> str:
    soup = BeautifulSoup(html["html"], "html.parser")

    # TODO Refactor these variable tests.
    _title = soup.find("h1", class_=re.compile(f"(?:^|){TITLE_CLASS}(?:$|)"))
    if _title and isinstance(_title, bs4.element.Tag):
        title = _title.get_text(strip=True)
    else:
        print(ERROR_DESCRIPTION)

    _location = soup.find("span", class_=re.compile(f"(?:^|){LOCATION_CLASS}(?:$|)"))
    if _location and isinstance(_location, bs4.element.Tag):
        location = _location.get_text(strip=True)
    else:
        print(ERROR_DESCRIPTION)

    _description = soup.find("div", class_=re.compile(f"(?:^|){DESCRIPTION_CLASS}(?:$|)"))
    if _description and isinstance(_description, bs4.element.Tag):
        _description_tag = _description.find("span")
        _description_markdown = md(str(_description_tag), newline_style="BACKSLASH")
        description = _description_markdown
    else:
        print(ERROR_DESCRIPTION)

    _company_logo = soup.find("img", class_=re.compile(f"(?:^|){IMAGE_CLASS}(?:$|)"))
    if _company_logo and isinstance(_company_logo, bs4.element.Tag):
        company_logo = str(_company_logo["src"])
    else:
        print(ERROR_DESCRIPTION)

    _company_url = soup.find("div", class_=re.compile(f"(?:^|){COMPANY_URL_CLASS}(?:$|)"))
    if _company_url and isinstance(_company_url, bs4.element.Tag):
        _company_url_tag = _company_url.find("a")
        if _company_url_tag and isinstance(_company_url_tag, bs4.element.Tag):
            company_url = str(_company_url_tag["href"])
        else:
            print(ERROR_DESCRIPTION)
    else:
        print(ERROR_DESCRIPTION)

    _subtitle = soup.find("div", class_=re.compile(f"(?:^|){SUBTITLE_CLASS}(?:$|)"))
    if _subtitle and isinstance(_subtitle, bs4.element.Tag):
        _subtitle_children = _subtitle.findChildren()
        company = _subtitle_children[0].get_text(strip=True)
    else:
        print(ERROR_DESCRIPTION)

    _highlight = soup.find("li", class_=re.compile(f"(?:^|){HIGHLIGHT_INSIGHT_CLASS}(?:$|)"))
    if _highlight and isinstance(_highlight, bs4.element.Tag):
        _highlight_tag = _highlight.find("span")
        if _highlight_tag and isinstance(_highlight_tag, bs4.element.Tag):
            _highlight_children = _highlight_tag.findChildren()
            workplace_type = _highlight_children[0].get_text(strip=True)
            contract_type = _highlight_children[1].get_text(strip=True)
            experience_level = _highlight_children[2].get_text(strip=True)
    else:
        print(ERROR_DESCRIPTION)

    result = LinkedInJobPost(
        workplace_type=workplace_type,
        contract_type=contract_type,
        experience_level=experience_level,
        company=company,
        company_url=company_url,
        location=location,
        title=title,
        company_logo=company_logo,
        description=description,
    )
    return result.model_dump_json()


# Scrape LinkedIn Job Post via Chrome extension.
# END


def extract_text_from_pdf(file: Path) -> str:
    try:
        reader = PdfReader(file)
        text = ""
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text += page.extract_text()
    except Exception as e:
        print("Error processing file: ", str(e))
        sys.exit(1)
    else:
        return text


ConfigType = Literal["models"]


def load_config(config: ConfigType) -> dict:
    with Path.open(CONFIG_FOLDER / f"{config}.yaml") as file:
        loaded_config: dict = yaml.safe_load(file)
    return loaded_config


def check_mps_backend() -> torch.Tensor | str:
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        x = torch.ones(1, device=mps_device)
        print("MPS device found:")
        print(x)
        return x
    else:
        print("MPS device not found!")
        return "MPS device not found"
