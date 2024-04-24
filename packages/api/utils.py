import re
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

import bs4
from bs4 import BeautifulSoup

from exceptions import AddBlanklineAfterStrong, InvalidInputError
from models import LinkedInJobPost


def create_job_posting(html: dict) -> str:
    soup = BeautifulSoup(html["html"], "html.parser")
    for s in soup.find_all(["script", "form"]):
        s.extract()
    text = soup.get_text(" ", strip=True)
    return text


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


ElementType = bs4.element.Tag | bs4.element.NavigableString | None



def md(html, **options):  # type: ignore[no-untyped-def]
    return AddBlanklineAfterStrong(**options).convert(html)


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


def scrape_from_linkedin(data: dict) -> LinkedInJobPost:  # type: ignore[return]
    soup = BeautifulSoup(data["html"], "html.parser")

    # Job url. Doing some cleaning first.
    _url = urlparse(data["url"])
    if _url.query and "currentJobId" in parse_qs(_url.query):
        url = "https://www.linkedin.com/jobs/view/" + parse_qs(_url.query)["currentJobId"][0]
    else:
        url = _url.scheme + "://" + _url.netloc + _url.path

    title = get_text(soup.find(["h1", "span"], class_=re.compile(f"(?:^|){TITLE_CLASS}(?:$|)")), "Job title")

    # Location: City, Region, Country format (LinkedIn)
    location = get_text(soup.find("span", class_=re.compile(f"(?:^|){LOCATION_CLASS}(?:$|)")), "Job location")

    # Job description
    description = md(
        str(soup.find("div", class_=re.compile(f"(?:^|){DESCRIPTION_CLASS}(?:$|)"))), newline_style="BACKSLASH"
    )

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
    _highlight_text = get_text(_highlight, "Parent node for workplace type, contract type and experience level")
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
