import uuid
from src.core.base_scraper import BaseScraper
from src.models.job import JobModel

class SmartRecruitersScraper(BaseScraper):
    def __init__(self, repository, company_name, url):
        super().__init__(repository)
        self.company_name = company_name
        self.url = url

    async def scrape(self):
        page = await self.start_browser(headless=True)
        try:
            print(f"[*] Starting SmartRecruiters scan for: {self.company_name}")
            await page.goto(self.url, wait_until='domcontentloaded')
            rows = await page.query_selector_all('.jobs-item')
            print(f"[+] Found {len(rows)} items.")
            for r in rows:
                title_el = await r.query_selector('h4')
                title = await title_el.inner_text() if title_el else "Unknown"
                link_el = await r.query_selector('a')
                href = await link_el.get_attribute('href') if link_el else ""
                job = JobModel(
                    job_id=f"SR-{self.company_name[:3].upper()}-{uuid.uuid4().hex[:6]}",
                    title=title.strip(),
                    company=self.company_name,
                    link=href,
                    location="Israel"
                )
                self.handle_found_job(job)
        except Exception as e:
            print(f"[!] SmartRecruiters error for {self.company_name}: {e}")
        finally:
            await self.close_browser()
