from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_name}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_user}"                 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor
# def connect_to_db(tries: int = 10, sleep: int = 2):
#     conn_try = 0 
#     while conn_try < tries:
#         try:
#             conn = psycopg2.connect(host="localhost", dbname="postgres",
#                                     user="postgres",
#                                     password="postgres",
#                                     cursor_factory=RealDictCursor)
#             cursor = conn.cursor()
#             print("--> Connected to database...")
#             break
#         except Exception as err:
#             conn_try += 1
#             print(f"--> Try {conn_try}/10. Could not connect to database with error: {err}")
#             time.sleep(sleep)
#         if conn_try == 10:
#                 print("--> Finally cannot connect to database.")  -----> not needed with alembic used

