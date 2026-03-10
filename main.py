import asyncio
from src.core.factory import AppFactory

async def run_discovery():
    scrapers = AppFactory.get_all_scrapers()
    
    for scraper in scrapers:
        scraper_name = scraper.__class__.__name__
        print(f"--- Starting {scraper_name} ---")
        try:
            await scraper.scrape()
        except Exception as e:
            print(f"Error in {scraper_name}: {e}")
        print(f"--- Finished {scraper_name} ---")

if __name__ == "__main__":
    asyncio.run(run_discovery())