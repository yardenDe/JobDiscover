from src.scrapers.base_scraper import BaseScraper

class SmartRecruitersScraper(BaseScraper):
    def extract_jobs(self, soup):
        found_jobs = []
        postings = soup.select('.job-item')
        for p in postings:
            link_el = p.select_one('a')
            url = link_el['href'] if link_el else ""
            ext_id = url.split('/')[-1] if url else None
            found_jobs.append({
                "title": p.select_one('.job-title').text.strip() if p.select_one('.job-title') else None,
                "url": url,
                "external_id": ext_id
            })
        return found_jobs
