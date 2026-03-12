from src.scrapers.base_scraper import BaseScraper

class SparkhireScraper(BaseScraper):
    def extract_jobs(self, soup):
        found_jobs = []
        jobs = soup.select('.job-listing') # Assuming standard Sparkhire listing class
        for j in jobs:
            title_el = j.select_one('.job-title a')
            url = title_el['href'] if title_el else ""
            # Extracting ID from URL like /job/view/12345
            ext_id = url.rstrip('/').split('/')[-1] if url else None
            found_jobs.append({
                "title": title_el.text.strip() if title_el else None,
                "url": url,
                "external_id": ext_id
            })
        return found_jobs
