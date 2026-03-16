from fastapi import APIRouter, HTTPException

from app.schemas import PostAdd, PostGet, PostUpdate
from app.services import PostsService


posts = APIRouter(prefix='/posts', tags=['Posts'])


@posts.post('/', summary='Create post')
async def add_post(post: PostAdd) -> dict:
    res = await PostsService().add_post(post)

    if res['status'] == 201:
        return res

    raise HTTPException(status_code=500, detail=res['detail'])


@posts.get('/', response_model=list[PostGet], summary='Get all posts')
async def get_posts(limit: int = 50) -> list['PostGet']:
    res = await PostsService().get_all(limit)

    if res['status'] == 200:
        return res['detail']

    raise HTTPException(status_code=500, detail=res['detail'])

    
@posts.get('/{post_id}', response_model=PostGet, summary='Get post by id')
async def get_post_by_id(post_id: int) -> 'PostGet':
    res = await PostsService().get_post_by_id(post_id)

    if res['status'] == 200:
        return res['detail']
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])


@posts.get('/user/{user_id}', response_model=list[PostGet], summary='Get posts at user')
async def get_posts_at_user(user_id: int) -> list['PostGet']:
    res = await PostsService().get_posts_at_user(user_id)

    if res['status'] == 200:
        return res['detail']

    raise HTTPException(status_code=500, detail=res['detail'])


@posts.put('/{post_id}', summary='Update post')
async def update_post(upd_data: PostUpdate, post_id: int) -> dict:
    res = await PostsService().update_post(upd_data, post_id)

    if res['status'] == 200:
        return res
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])


@posts.delete('/{post_id}', summary='Delete post')
async def delete_post(post_id: int) -> dict:
    res = await PostsService().delete_post(post_id)

    if res['status'] == 200:
        return res
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])
