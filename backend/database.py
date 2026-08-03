"""Module Establishes Database Connection"""

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Select, or_
from sqlalchemy.orm import sessionmaker, Session, declarative_base, selectinload

load_dotenv()

db_url = os.environ.get("DATABASE_URL")


engine = create_engine(db_url)
SESSIONLOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getdb():


    db = SESSIONLOCAL()
    try:
        yield db
    finally:
        db.close()
