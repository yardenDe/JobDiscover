from src.core.database import DBManager
from src.models.job import JobModel

class JobRepository:
    def __init__(self, db: DBManager):
        self.db = db
        self._init_table()

    def _init_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            link TEXT,
            location TEXT,
            discovered_at TIMESTAMP
        );
        """
        self.db.execute(query)

    def is_new(self, job_id: str) -> bool:
        query = "SELECT 1 FROM jobs WHERE job_id = :id"
        return self.db.fetch_one(query, {"id": job_id}) is None

    def add_job(self, job: JobModel):
        query = """
        INSERT INTO jobs (job_id, title, company, link, location, discovered_at)
        VALUES (:job_id, :title, :company, :link, :location, :discovered_at)
        ON CONFLICT(job_id) DO NOTHING
        """
        self.db.execute(query, job.model_dump())