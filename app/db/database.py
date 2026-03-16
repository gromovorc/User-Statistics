from sqlalchemy import create_engine, MetaData

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

metadata = MetaData()

def get_connection():
    with engine.connect() as conn:
        yield conn