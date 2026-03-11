import uuid
from src.core.base_scraper import BaseScraper
from src.models.job import JobModel

class WorkdayScraper(BaseScraper):
    def __init__(self, repository, company_name, url):
        super().__init__(repository)
        self.company_name = company_name
        self.url = url

    async def scrape(self):
        page = await self.start_browser(headless=True)
        try:
            print(f"[*] Starting Workday scan for: {self.company_name}")
            await page.goto(self.url, wait_until='networkidle')
            job_cards = await page.query_selector_all('[data-automation-id=\"jobResultItem\"]')
            print(f"[+] Found {len(job_cards)} items.")
            for card in job_cards:
                title_el = await card.query_selector('[data-automation-id=\"jobTitle\"]')
                title = await title_el.inner_text() if title_el else "Unknown"
                location_el = await card.query_selector('[data-automation-id=\"locations\"]')
                location = await location_el.inner_text() if location_el else "Israel"
                job = JobModel(
                    job_id=f"WD-{self.company_name[:3].upper()}-{uuid.uuid4().hex[:6]}",
                    title=title.strip(),
                    company=self.company_name,
                    link=self.url,
                    location=location.strip()
                )
                self.handle_found_job(job)
        except Exception as e:
            print(f"[!] Workday error for {self.company_name}: {e}")
        finally:
            await self.close_browser()
