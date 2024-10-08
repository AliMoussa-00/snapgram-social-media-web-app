#!/usr/bin/env python3
""" FastApi server. """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.engine.db_storage import init_db
from app.api.routes.posts import post_router
from app.api.routes.comments import comment_router
from app.api.routes.likes import like_router

from app.api.routes.users import user_router   # router as Router
from app.api.auth.auth import auth_router  # router as AuthRouter


app = FastAPI()

# Adding Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=['Auth'], prefix='/auth')
app.include_router(user_router, tags=['Users'], prefix='/users')
app.include_router(post_router, tags=['Posts'], prefix='/posts')
app.include_router(comment_router, tags=['Comments'], prefix='/comments')
app.include_router(like_router, tags=['Likes'], prefix='/likes')


@app.on_event('startup')
async def on_startup():
    """
    Initialize MongoDB connection during application startup.
    This function connects to MongoDB using the provided MONGODB_URL.
    """
    await init_db()


@app.get('/', tags=['Root'])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie powered app!"}

if __name__ == '__main__':
    import uvicorn
    from core.config import CONFIG
    uvicorn.run(app, host=CONFIG.host, port=CONFIG.port)
