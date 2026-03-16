from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.api import users, posts, comments, seed_database_sqlalchemy
from app.db import engine, Base

import uvicorn



async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print('DB created')

    await seed_database_sqlalchemy()
    print('DB insert')

    yield


app = FastAPI(
    title='Blog API', description='API for blog app', version='0.0.1', lifespan=lifespan
)


@app.get('/', tags=['Root'])
async def root():
    return {'documentation': '/docs', 'version': '0.0.1'}


app.include_router(users)
app.include_router(posts)
app.include_router(comments)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
