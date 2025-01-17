import re
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urljoin, urlparse

from models import LinkedInJobPost
from .md_utils import md

from .bs_utils import get_text, check_el_type, return_first_match
from .constants import *

class LinkedInScraper:
    def __init__(self, data: dict):
        self.soup = BeautifulSoup(data["html"], "html.parser")
        self.url = data["url"]
        
    def get_job_url(self) -> str:
        _url = urlparse(self.url)
        if _url.query and "currentJobId" in parse_qs(_url.query):
            return "https://www.linkedin.com/jobs/view/" + parse_qs(_url.query)["currentJobId"][0]
        return f"{_url.scheme}://{_url.netloc}{_url.path}"
    
    def get_location(self) -> str:
        location_div = self.soup.find("div", class_=re.compile(f"(?:^|){LOCATION_CLASS}(?:$|)"))
        return get_text(
            check_el_type(location_div, "Company profile url").find_all("span")[0],
            "Job location"
        )
    
    def get_company_url(self) -> str:
        _company_url = self.soup.find("div", class_=re.compile(f"(?:^|){COMPANY_URL_CLASS}(?:$|)"))
        _company_url_tag = check_el_type(_company_url, "Company profile url").find("a")
        _company_url_full = check_el_type(_company_url_tag, "Company profile url")["href"]
        _company_url_parsed = urlparse(str(_company_url_full))
        _company_url_new_path = "/".join(_company_url_parsed.path.split("/")[:-1])
        return urljoin(str(_company_url_full), _company_url_new_path)
    
    def get_job_details(self) -> dict:
        _highlight = self.soup.find("li", class_=re.compile(f"(?:^|){HIGHLIGHT_INSIGHT_CLASS}(?:$|)"))
        _highlight_text = get_text(_highlight, "Parent node for workplace type, contract type and experience level")
        
        return {
            "contract_type": return_first_match(_highlight_text, CONTRACT_TYPE_REGEX),
            "experience_level": return_first_match(_highlight_text, EXPERIENCE_LEVEL_REGEX),
            "workplace_type": return_first_match(_highlight_text, WORKPLACE_TYPE_REGEX)
        }
    
    def scrape(self) -> LinkedInJobPost:
        job_details = self.get_job_details()
        
        return LinkedInJobPost(
            company_logo=str(check_el_type(
                self.soup.find("img", class_=re.compile(f"(?:^|){IMAGE_CLASS}(?:$|)")),
                "Company logo"
            )["src"]),
            company=get_text(
                self.soup.find("div", "a", class_=re.compile(f"(?:^|){COMPANY_URL_CLASS}(?:$|)")),
                "Job location"
            ),
            title=get_text(
                self.soup.find(["div","h1"], class_=re.compile(f"(?:^|){TITLE_CLASS}(?:$|)")),
                "Job title"
            ),
            description=md(
                str(self.soup.find("div", class_=re.compile(f"(?:^|){DESCRIPTION_CLASS}(?:$|)"))),
                newline_style="BACKSLASH"
            ),
            experience_level=job_details["experience_level"],
            contract_type=job_details["contract_type"],
            location=self.get_location(),
            workplace_type=job_details["workplace_type"],
            url=self.get_job_url(),
            company_url=self.get_company_url()
        )