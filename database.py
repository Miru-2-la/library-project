from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# using sqlite because it's zero setup
DB_PATH = 'sqlite:///./library.db'

engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def open_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
