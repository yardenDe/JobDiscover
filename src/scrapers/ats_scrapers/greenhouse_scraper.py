from src.scrapers.base_scraper import BaseScraper

class GreenhouseScraper(BaseScraper):
    def extract_jobs(self, soup):
        found_jobs = []
        postings = soup.select('.opening')
        for p in postings:
            title_el = p.find('a')
            ext_id = p.get('gh_jid') or (title_el['href'].split('/')[-1] if title_el else None)
            found_jobs.append({
                "title": title_el.text.strip() if title_el else None,
                "url": "https://boards.greenhouse.io" + title_el['href'] if title_el else None,
                "external_id": ext_id
            })
        return found_jobs
