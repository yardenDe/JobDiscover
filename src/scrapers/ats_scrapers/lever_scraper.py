import uuid
from src.core.base_scraper import BaseScraper
from src.models.job import JobModel

class LeverScraper(BaseScraper):
    def __init__(self, repository, company_name, url):
        super().__init__(repository)
        self.company_name = company_name
        self.url = url

    async def scrape(self):
        page = await self.start_browser(headless=True)
        try:
            print(f"[*] Starting Lever scan for: {self.company_name}")
            await page.goto(self.url, wait_until='domcontentloaded')
            postings = await page.query_selector_all('.posting')
            print(f"[+] Found {len(postings)} items.")
            for p in postings:
                title_el = await p.query_selector('h5')
                title = await title_el.inner_text() if title_el else "Unknown"
                link_el = await p.query_selector('a.posting-title')
                link = await link_el.get_attribute('href') if link_el else self.url
                job = JobModel(
                    job_id=f"LV-{self.company_name[:3].upper()}-{uuid.uuid4().hex[:6]}",
                    title=title.strip(),
                    company=self.company_name,
                    link=link,
                    location="Israel"
                )
                self.handle_found_job(job)
        except Exception as e:
            print(f"[!] Lever error for {self.company_name}: {e}")
        finally:
            await self.close_browser()
