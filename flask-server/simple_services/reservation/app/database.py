from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# DB_SERVER = os.getenv("DB_SERVER")
# DB_PORT = os.getenv("DB_PORT")
# DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# DATABASE = os.getenv("DATABASE")
DATABASE = "reservation"


# SQLALCHEMY_DATABASE_URL = (
#     f"mysql+mysqlconnector://root:root@host.docker.internal:9999/reservations"
# )
#SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:8889/reservations'
SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:3306/reservation'

print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()