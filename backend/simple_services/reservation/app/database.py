from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# SQLALCHEMY_DATABASE_URL = (
#     f"mysql+mysqlconnector://root:root@host.docker.internal:9999/reservations"
# )
#SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:8889/reservations'
db_host = os.getenv("RESERVATION_MYSQL_DATABASE")
db_port = os.getenv("MYSQL_PORT") 
db_pwd = os.getenv("MYSQL_ROOT_PASSWORD") 

dbURL = f'mysql+mysqlconnector://root:{db_pwd}@{db_host}:{db_port}/reservation'


engine = create_engine(dbURL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()