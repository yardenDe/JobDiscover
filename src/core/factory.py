import os
from dotenv import load_dotenv
from src.core.db_manager import DBManager
from src.repositories.job_repository import JobRepository

load_dotenv()

class AppFactory:
    _db_instance = None
    _repo_instance = None

    @staticmethod
    def get_db_manager() -> DBManager:
        if AppFactory._db_instance is None:
            url = os.getenv("DATABASE_URL", "sqlite:///jobs.db")
            AppFactory._db_instance = DBManager(url)
        return AppFactory._db_instance

    @staticmethod
    def get_job_repository() -> JobRepository:
        if AppFactory._repo_instance is None:
            db = AppFactory.get_db_manager()
            AppFactory._repo_instance = JobRepository(db)
        return AppFactory._repo_instance

    @staticmethod
    def get_all_scrapers() -> list:

        repo = AppFactory.get_job_repository()
        