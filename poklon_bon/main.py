from fastapi import FastAPI
from . import models
from .database import engine

from .routers import bon, user, auth

app = FastAPI(title="Sistem za Poklon BONOVE")

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

app.include_router(bon.router)

app.include_router(user.router)

