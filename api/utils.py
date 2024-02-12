import json
import re
import sys
from pathlib import Path
from typing import Any, Literal

import torch
import yaml
from bs4 import BeautifulSoup
from jsonref import replace_refs
from PyPDF2 import PdfReader

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
