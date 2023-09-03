from fastapi import FastAPI
from .routers import media, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "98.191.38.24",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(media.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
