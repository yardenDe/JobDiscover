from sqlalchemy import create_engine, text

class DBManager:
    def __init__(self, database_url):
        self.database_url = database_url
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.database_url)
        return self._engine

    def fetch_all(self, query, params=None) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row) for row in result.mappings()]

    def fetch_one(self, query, params=None) -> dict:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            row = result.mappings().first()
            return dict(row) if row else None

    def execute(self, query, params=None):
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})