import uuid
from src.core.base_scraper import BaseScraper
from src.models.job import JobModel

class SparkHireScraper(BaseScraper):
    def __init__(self, repository, company_name, url):
        super().__init__(repository)
        self.company_name = company_name
        self.url = url

    async def scrape(self):
        page = await self.start_browser(headless=True)
        try:
            print(f"[*] Starting SparkHire/Comeet scan for: {self.company_name}")
            await page.goto(self.url, wait_until="networkidle")
            
            # This selector covers both Comeet (.position-item) and Spark Hire (.job-item)
            job_elements = await page.query_selector_all('.position-item, .job-item, .position-row')
            print(f"[+] Found {len(job_elements)} potential jobs.")
            
            for el in job_elements:
                title_el = await el.query_selector('h4, .position-name, .title')
                title = await title_el.inner_text() if title_el else "Unknown Title"
                
                link_el = await el.query_selector('a')
                href = await link_el.get_attribute('href') if link_el else ""
                
                # Logic to handle both relative and absolute links
                full_link = href if href.startswith('http') else f"https://www.comeet.com{href}"

                job = JobModel(
                    job_id=f"SH-{self.company_name[:3].upper()}-{uuid.uuid4().hex[:6]}",
                    title=title.strip(),
                    company=self.company_name,
                    link=full_link,
                    location="Israel"
                )
                self.handle_found_job(job)
        except Exception as e:
            print(f"[!] SparkHire/Comeet error for {self.company_name}: {e}")
        finally:
            await self.close_browser()