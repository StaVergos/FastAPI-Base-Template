from app.core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

database_url = config.DATABASE_URL

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
