import asyncio

class DiscoveryService:
    def __init__(self, factory, max_concurrent=3):
        self.factory = factory
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def _run_with_semaphore(self, scraper, company, url):
        async with self.semaphore:
            try:
                await scraper.run(company_name=company, url=url)
            except Exception as e:
                print(f"Error running scraper for {company}: {e}")

    async def start_discovery(self, targets):
        tasks = []
        for target in targets:
            try:
                scraper = self.factory.create_scraper(target['platform'])
                
                tasks.append(self._run_with_semaphore(
                    scraper, 
                    target['company'], 
                    target['url']
                ))
            except Exception as e:
                print(f"Skipping {target.get('company', 'Unknown')}: {e}")
        
        if tasks:
            await asyncio.gather(*tasks)