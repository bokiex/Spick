from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = os.getenv("dbURL")
SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root@localhost:3306/event'
db_host = os.getenv("EVENT_MYSQL_DATABASE")
db_port = os.getenv("MYSQL_PORT") 
db_pwd = os.getenv("MYSQL_ROOT_PASSWORD") 

dbURL = f'mysql+mysqlconnector://root:{db_pwd}@{db_host}:{db_port}/event'


engine = create_engine(dbURL, echo=True)  #changed back to DATABASE_URL if needed

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()