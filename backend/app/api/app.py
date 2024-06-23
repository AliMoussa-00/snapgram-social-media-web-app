#!/usr/bin/env python3
""" FastApi server. """

from fastapi import FastAPI
from app.models.engine.db_storage import init_db
from app.api.routes.posts import post_router


app = FastAPI()
app.include_router(post_router, tags=['Post'], prefix='/posts')


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
    from core.config import HOST, PORT
    uvicorn.run(app, host=HOST, port=PORT)
