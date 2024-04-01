from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# SQLALCHEMY_DATABASE_URL = os.getenv("dbURL")
# SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://is213@host.docker.internal:3306/user_schedule'
# SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:3306/event'
db_host = os.getenv("USER_SCHEDULE_MYSQL_DATABASE")
db_port = os.getenv("MYSQL_PORT") 
db_pwd = os.getenv("MYSQL_ROOT_PASSWORD") 

dbURL = f'mysql+mysqlconnector://root:{db_pwd}@{db_host}:{db_port}/user_schedule'
print(dbURL)

engine = create_engine(dbURL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()