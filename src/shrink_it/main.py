from fastapi import FastAPI
from .database import Base, engine
from .urls import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def test():
    return {
        "message": "test"
    }