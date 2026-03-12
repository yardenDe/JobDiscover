from src.scrapers.base_scraper import BaseScraper

class LeverScraper(BaseScraper):
    def extract_jobs(self, soup):
        found_jobs = []
        postings = soup.select('.posting')
        for p in postings:
            link_el = p.select_one('a.posting-title')
            url = link_el['href'] if link_el else ""
            ext_id = url.split('/')[-1] if url else None
            found_jobs.append({
                "title": p.find('h5').text.strip() if p.find('h5') else None,
                "url": url,
                "external_id": ext_id
            })
        return found_jobs
