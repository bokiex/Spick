from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from contextlib import contextmanager
load_dotenv()
import os


# SQLALCHEMY_DATABASE_URL = os.getenv("dbURL")
SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:3306/user'
#SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:8889/user'
# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def SessionManager():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()