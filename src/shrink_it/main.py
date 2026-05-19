from fastapi import FastAPI
from .database import Base, engine
from .urls.router import router as urls_router
from .users.router import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(urls_router)
app.include_router(users_router)
