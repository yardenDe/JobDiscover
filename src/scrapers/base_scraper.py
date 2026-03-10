from abc import ABC, abstractmethod
from playwright.async_api import async_playwright
from src.repositories.job_repository import JobRepository
from src.models.job import JobModel

class BaseScraper(ABC):
    def __init__(self, repository: JobRepository):
        self.repository = repository
        self.playwright = None
        self.browser = None
        self.context = None

    @abstractmethod
    async def scrape(self):
        pass

    async def start_browser(self, headless: bool = True):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        return await self.context.new_page()

    async def close_browser(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def handle_found_job(self, job: JobModel):
        if self.repository.is_new(job.job_id):
            self.repository.add_job(job)
            print(f"New job found: {job.title} at {job.company}")
        else:
            print(f"Job already exists: {job.job_id}")