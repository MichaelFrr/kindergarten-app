from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base


DATABASE_URL = "postgresql://postgres:0@localhost:5432/kindergarten_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getdb():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
