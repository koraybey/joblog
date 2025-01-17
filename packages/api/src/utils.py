from models import LinkedInJobPost
from scraper.linkedin import LinkedInScraper

def scrape_from_linkedin(data: dict) -> LinkedInJobPost:
    scraper = LinkedInScraper(data)
    return scraper.scrape()