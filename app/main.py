import psycopg
from fastapi import FastAPI
from .dbConnect import engine, Base
from .routers import media, user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()


DB_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
try:
    conn = psycopg.connect(DB_URL)
    cur = conn.cursor()  # Define the cursor object at the module level
    print("DB connection was successful!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()


app.include_router(media.router)
app.include_router(user.router)
app.include_router(auth.router)
