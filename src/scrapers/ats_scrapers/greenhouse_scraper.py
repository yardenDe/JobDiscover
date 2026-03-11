import uuid
from src.core.base_scraper import BaseScraper
from src.models.job import JobModel

class GreenhouseScraper(BaseScraper):
    def __init__(self, repository, company_name, url):
        super().__init__(repository)
        self.company_name = company_name
        self.url = url

    async def scrape(self):
        page = await self.start_browser(headless=True)
        try:
            print(f"[*] Starting Greenhouse scan for: {self.company_name}")
            await page.goto(self.url, wait_until='domcontentloaded')
            openings = await page.query_selector_all('.opening')
            print(f"[+] Found {len(openings)} items.")
            for op in openings:
                link_el = await op.query_selector('a')
                title = await link_el.inner_text() if link_el else "Unknown"
                href = await link_el.get_attribute('href') if link_el else ""
                location_el = await op.query_selector('.location')
                loc = await location_el.inner_text() if location_el else "Israel"
                full_link = f"https://boards.greenhouse.io{href}" if href.startswith('/') else href
                job = JobModel(
                    job_id=f"GH-{self.company_name[:3].upper()}-{uuid.uuid4().hex[:6]}",
                    title=title.strip(),
                    company=self.company_name,
                    link=full_link,
                    location=loc.strip()
                )
                self.handle_found_job(job)
        except Exception as e:
            print(f"[!] Greenhouse error for {self.company_name}: {e}")
        finally:
            await self.close_browser()
