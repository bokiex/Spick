from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()
import os


# SQLALCHEMY_DATABASE_URL = os.getenv("dbURL")
# SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://is213@host.docker.internal:3306/user_schedule'
# SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:3306/event'

dbURL = os.getenv("SQLALCHEMY_DATABASE_URL") or 'mysql+mysqlconnector://is213@host.docker.internal:3306/user_schedule'


engine = create_engine(dbURL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()