from fastapi import FastAPI
from .dbConnect import engine, Base
from .routers import media, user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(media.router)
app.include_router(user.router)
app.include_router(auth.router)
