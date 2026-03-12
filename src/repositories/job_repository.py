from src.core.job_model import JobModel

class JobRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self._table_initialized = False

    def _ensure_table_exists(self):
        if not self._table_initialized:
            query = """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fingerprint TEXT UNIQUE,
                external_id TEXT,
                title TEXT,
                company TEXT,
                location TEXT,
                url TEXT,
                platform TEXT
            )
            """
            self.db_manager.execute(query)
            self._table_initialized = True

    def save_job(self, job: JobModel):
        self._ensure_table_exists()
        
        check_query = "SELECT 1 FROM jobs WHERE fingerprint = :fingerprint"
        if not self.db_manager.fetch_one(check_query, {"fingerprint": job.fingerprint}):
            insert_query = """
            INSERT INTO jobs (fingerprint, external_id, title, company, location, url, platform)
            VALUES (:fingerprint, :external_id, :title, :company, :location, :url, :platform)
            """
            self.db_manager.execute(insert_query, {
                "fingerprint": job.fingerprint,
                "external_id": job.external_id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "url": job.url,
                "platform": job.platform
            })