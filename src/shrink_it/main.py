from fastapi import FastAPI
from .database import Base, engine
from .urls import models
from .urls.router import router as urls_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(urls_router)
