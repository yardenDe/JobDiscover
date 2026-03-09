import os
from sqlalchemy import create_engine, text

class DBManager:
    def __init__(self, database_url: str):
        if not database_url:
            raise ValueError("Database URL is required")
        self.engine = create_engine(database_url)

    def execute(self, query: str, params: dict = None):
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})

    def fetch_all(self, query: str, params: dict = None) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row) for row in result.mappings().all()]

    def fetch_one(self, query: str, params: dict = None) -> dict:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            row = result.mappings().first()
            return dict(row) if row else None