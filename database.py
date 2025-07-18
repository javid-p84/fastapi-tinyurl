from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE_POSTGRES = "postgresql://postgres:password@localhost:5432/tinyurl"

engine = create_engine(URL_DATABASE_POSTGRES, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()