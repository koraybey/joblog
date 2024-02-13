import json
import re
import sys
from pathlib import Path
from typing import Any, Literal
from urllib.parse import parse_qs, urljoin, urlparse

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
TITLE_CLASS = "card__job-title"
LOCATION_CLASS = "card__bullet"
DESCRIPTION_CLASS = "jobs-description-content__text"
COMPANY_URL_CLASS = "primary-description-without-tagline"
HIGHLIGHT_INSIGHT_CLASS = "__job-insight--highlight"
SUBTITLE_CLASS = "primary-description-without-tagline"
CONTRACT_TYPE_REGEX = "(?:Full-time|Part-time|Contract|Internship)"
WORKPLACE_TYPE_REGEX = "(?:Remote|Hybrid|On-site)"
EXPERIENCE_LEVEL_REGEX = "(?:Internship|Entry|Associate|Mid-Senior|Director|Executive)"


VAR_ERRORS = LinkedInJobPost(
    company_logo="Company logo",
    company="Company name",
    title="Job title",
    description="Job description",
    experience_level="Experience level",
    contract_type="Contract type",
    location="Location",
    workplace_type="Workplace type",
    url="Job listing url",
    company_url="Company profile url",
)


# Markdown conversion helper functions.
class AddBlanklineAfterStrong(MarkdownConverter):  # type: ignore[no-any-unimported]
    """Custom MarkdownConverter that adds a blank line after <strong> tag."""

    def convert_strong(self, el, text, convert_as_inline):  # type: ignore[no-untyped-def]
        return super().convert_strong(el, text, convert_as_inline) + "\n\n"


# TODO Move exceptions somewhere else.
class InvalidInputError(Exception):
    """Raise error if DOM element is not found."""

    def __init__(self, el_name: str):
        super().__init__(f"{el_name} not found or tag type is invalid.")


def md(html, **options):  # type: ignore[no-untyped-def]
    return AddBlanklineAfterStrong(**options).convert(html)


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
        result = re.findall(regex,text)[0]
    except (Exception, IndexError):
        result = None
    return result


def scrape_from_linkedin(data: dict) -> LinkedInJobPost: #type: ignore[return]
    soup = BeautifulSoup(data["html"], "html.parser")

    # Job url. Doing some cleaning first.
    _url = urlparse(data["url"])
    if _url.query and "currentJobId" in parse_qs(_url.query):
        url = "https://www.linkedin.com/jobs/view/" + parse_qs(_url.query)["currentJobId"][0]
    else:
        url = _url.scheme + "://" + _url.netloc + _url.path

    # Job title
    _title = soup.find(["h1", "span"], class_=re.compile(f"(?:^|){TITLE_CLASS}(?:$|)"))
    title = get_text(_title, "Job title")

    # Location: City, Region, Country format (LinkedIn)
    _location = soup.find("span", class_=re.compile(f"(?:^|){LOCATION_CLASS}(?:$|)"))
    location = get_text(_location, "Job location")

    # Job description
    _description = soup.find("div", class_=re.compile(f"(?:^|){DESCRIPTION_CLASS}(?:$|)"))
    _description_tag = check_el_type(_description, "Job description").find("span")
    description = md(str(_description_tag), newline_style="BACKSLASH")

    # Company logo url
    _company_logo = soup.find("img", class_=re.compile(f"(?:^|){IMAGE_CLASS}(?:$|)"))
    company_logo = str(check_el_type(_company_logo, "Company logo")["src"])

    # Company profile url (LinkedIn)
    _company_url = soup.find("div", class_=re.compile(f"(?:^|){COMPANY_URL_CLASS}(?:$|)"))
    _company_url_tag = check_el_type(_company_url, "Company profile url").find("a")
    _company_url_full = check_el_type(_company_url_tag, "Company profile url")["href"]
    _company_url_parsed = urlparse(str(_company_url_full))

    # Scraped LinkedIn profile URL is https://www.linkedin.com/company/metacoregames/life/
    # We need the company page, so we are removing the last path
    _company_url_new_path = "/".join(_company_url_parsed.path.split("/")[:-1])
    company_url = urljoin(str(_company_url_full), _company_url_new_path)

    # Company name
    _subtitle = soup.find("div", class_=re.compile(f"(?:^|){SUBTITLE_CLASS}(?:$|)"))
    _subtitle_children = get_children(_subtitle, "Parent node for company name")
    company = get_text(_subtitle_children[0], "Company name")

    _highlight = soup.find("li", class_=re.compile(f"(?:^|){HIGHLIGHT_INSIGHT_CLASS}(?:$|)"))
    _highlight_text = get_text(
        _highlight, "Parent node for workplace type, contract type and experience level"
    )
    # Contract type: Full-time, Part-time, Contract, Internship (LinkedIn)
    contract_type = return_first_match(_highlight_text, CONTRACT_TYPE_REGEX)
    # Experience level: Internship, Entry, Associate, Mid-Senior, Director, Executive (LinkedIn)
    experience_level = return_first_match(_highlight_text, EXPERIENCE_LEVEL_REGEX)
    # Workplace type: Remote, Hybrid, On-site (LinkedIn)
    workplace_type = return_first_match(_highlight_text, WORKPLACE_TYPE_REGEX)

    return LinkedInJobPost(
        company_logo=company_logo,
        company=company,
        title=title,
        description=description,
        experience_level=experience_level,
        contract_type=contract_type,
        location=location,
        workplace_type=workplace_type,
        url=url,
        company_url=company_url,
    )


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
