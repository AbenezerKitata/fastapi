import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

DB_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# DB_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
# try:
#     conn = psycopg.connect(DB_URL)
#     cur = conn.cursor()  # Define the cursor object at the module level
#     print("DB connection was successful!")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
#     exit()
