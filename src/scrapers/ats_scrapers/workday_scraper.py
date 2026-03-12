from src.scrapers.base_scraper import BaseScraper
import re

class WorkdayScraper(BaseScraper):
    def extract_jobs(self, soup):
        found_jobs = []
        title_el = soup.select_one('[data-automation-id="jobPostingHeader"]')
        if title_el:
            text_content = soup.get_text()
            job_id_match = re.search(r'(JR|R)-\d+|[0-9]{5,10}', text_content)
            ext_id = job_id_match.group(0) if job_id_match else None
            found_jobs.append({
                "title": title_el.text.strip(),
                "external_id": ext_id
            })
        return found_jobs
