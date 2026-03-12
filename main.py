import asyncio
import json
import os
from src.core.db_manager import DBManager
from src.repositories.job_repository import JobRepository
from src.services.factory import Factory
from src.services.discovery import DiscoveryService

async def main():
    # 1. Initialize Infrastructure
    db_manager = DBManager("jobs.db")
    repository = JobRepository(db_manager)
    
    # 2. Initialize Services
    factory = Factory(repository)
    discovery = DiscoveryService(factory)

    # 3. Load Targets from JSON
    targets_path = "targets.json"
    if not os.path.exists(targets_path):
        print(f"[!] Error: {targets_path} not found.")
        return

    with open(targets_path, 'r', encoding='utf-8') as f:
        targets = json.load(f)

    # 4. Run Discovery
    print(f"[*] Loaded {len(targets)} targets. Starting discovery...")
    await discovery.start_discovery(targets)
    print("[*] Discovery process completed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    except Exception as e:
        print(f"\n[!] Critical error: {e}")