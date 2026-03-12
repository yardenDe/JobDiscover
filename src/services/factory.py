from src.scrapers.ats_scrapers.greenhouse_scraper import GreenhouseScraper
from src.scrapers.ats_scrapers.lever_scraper import LeverScraper
from src.scrapers.ats_scrapers.smart_recruiters_scraper import SmartRecruitersScraper
from src.scrapers.ats_scrapers.sparkhire_scraper import SparkHireScraper
from src.scrapers.ats_scrapers.workday_scraper import WorkdayScraper

class Factory:
    def __init__(self, repository):
        self.repository = repository
        self._mapping = {
            "greenhouse": GreenhouseScraper,
            "lever": LeverScraper,
            "smart_recruiters": SmartRecruitersScraper,
            "sparkhire": SparkHireScraper,
            "workday": WorkdayScraper
        }

    def create_scraper(self, platform: str):
        platform_key = platform.lower().strip()
        scraper_class = self._mapping.get(platform_key)
        
        if not scraper_class:
            raise ValueError(f"Unsupported platform: {platform}")
            
        return scraper_class(self.repository)