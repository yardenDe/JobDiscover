import hashlib
from abc import ABC, abstractmethod
from playwright.async_api import async_playwright
from src.core.job_model import JobModel
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    def __init__(self, repository):
        self.repository = repository

    @abstractmethod
    def extract_jobs(self, soup) -> list[dict]:
        pass

    def _generate_fingerprint(self, platform, external_id, title, company):
        if external_id:
            raw_key = f"{platform}_{external_id}"
        else:
            raw_key = f"{platform}_{company}_{title}".lower().replace(" ", "")
        return hashlib.md5(raw_key.encode()).hexdigest()

    async def run(self, company_name, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent="Mozilla/5.0")
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                jobs_data = self.extract_jobs(soup)
                platform_name = self.__class__.__name__.replace("Scraper", "").lower()
                
                for data in jobs_data:
                    fingerprint = self._generate_fingerprint(
                        platform_name, 
                        data.get('external_id'),
                        data.get('title'),
                        company_name
                    )
                    
                    job = JobModel(
                        title=data.get('title'),
                        company=company_name,
                        location=data.get('location', 'Israel'),
                        url=data.get('url', url),
                        platform=platform_name,
                        external_id=data.get('external_id'),
                        fingerprint=fingerprint
                    )
                    self.handle_found_job(job)
                    
            except Exception as e:
                print(f"Error scraping {company_name}: {str(e)}")
            finally:
                await browser.close()

    def handle_found_job(self, job: JobModel):
        if job.title:
            print(f"[+] Found: {job.title} @ {job.company}")
            self.repository.save_job(job)