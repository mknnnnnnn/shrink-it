from fastapi import FastAPI

from .auth.router import router as auth_router
from .urls.router import redirect_router
from .urls.router import router as urls_router
from .users.router import router as users_router

app = FastAPI()

app.include_router(urls_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(redirect_router)
