from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path

script_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=script_dir / ".env")

db_url = os.environ.get("DATABASE_URL")


engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getdb():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
