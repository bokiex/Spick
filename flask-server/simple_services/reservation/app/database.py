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
DATABASE_URL = os.getenv("DATABASE_URL")


# SQLALCHEMY_DATABASE_URL = (
#     f"mysql+mysqlconnector://root:root@host.docker.internal:9999/reservations"
# )
#SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://is213@localhost:8889/reservations'


engine = create_engine(DATABASE_URL, echo=True)
print(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()