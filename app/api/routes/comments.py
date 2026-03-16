from fastapi import APIRouter, HTTPException

from app.schemas import CommentAdd, CommentGet, CommentUpdate
from app.services import CommentsService


comments = APIRouter(prefix='/comments', tags=['Comments'])


@comments.post('/', summary='Create comment')
async def add_comment(comment: CommentAdd) -> dict:
    res = await CommentsService().add_comment(comment)

    if res['status'] == 201:
        return res

    raise HTTPException(status_code=500, detail=res['detail'])


@comments.get('/post/{post_id}', response_model=list[CommentGet], summary='Get comments at post')
async def get_comments_at_post(post_id: int) -> list['CommentGet']:
    res = await CommentsService().get_comments_at_post(post_id)

    if res['status'] == 200:
        return res['detail']

    raise HTTPException(status_code=500, detail=res['detail'])


@comments.get('/{comment_id}', response_model=CommentGet, summary='Get comment by id')
async def get_comment_by_id(comment_id: int) -> 'CommentGet':
    res = await CommentsService().get_comment_by_id(comment_id)

    if res['status'] == 200:
        return res['detail']
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])


@comments.put('/{comment_id}', summary='Update comment')
async def update_comment(comment: CommentUpdate, comment_id: int) -> dict:
    res = await CommentsService().update_comment(comment, comment_id)

    if res['status'] == 200:
        return res
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])


@comments.delete('/{comment_id}', summary='Delete comment')
async def delete_comment(comment_id: int) -> dict:
    res = await CommentsService().delete_comment(comment_id)

    if res['status'] == 200:
        return res
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])
