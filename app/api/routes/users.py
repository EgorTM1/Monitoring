from fastapi import APIRouter, HTTPException

from app.schemas import UserGet, UserAdd, UserUpdate, UserGetDTO
from app.services import UsersService


users = APIRouter(prefix='/users', tags=['Users'])


@users.get('/', response_model=list[UserGet], summary='Get all users')
async def get_users(limit: int = 50) -> list['UserGet']:
    res = await UsersService().get_all(limit=limit)

    if res['status'] == 200:
        return res['detail']

    raise HTTPException(status_code=500, detail=res['detail'])


@users.post('/', summary='Create user')
async def create_user(user: UserAdd) -> dict:
    res = await UsersService().add_user(user=user)

    if res['status'] == 201:
        return res

    raise HTTPException(status_code=500, detail=res['detail'])


@users.get('/with-rel', response_model=list[UserGetDTO], summary='Get all users with relations')
async def get_all_with_rel() -> list['UserGetDTO']:
    res = await UsersService().get_all_with_rel()

    if res['status'] == 200:
        return res['detail']

    raise HTTPException(status_code=500, detail=res['detail'])



@users.get('/{user_id}', response_model=UserGet, summary='Get user by id')
async def get_user_by_id(user_id: int) -> 'UserGet':
    res = await UsersService().get_user_by_id(user_id=user_id)

    if res['status'] == 200:
        return res['detail']
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])


@users.put('/{user_id}', summary='Update user')
async def update_user(upd_data: UserUpdate, user_id: int) -> dict:
    res = await UsersService().update_user(upd_data=upd_data, user_id=user_id)

    if res['status'] == 200:
        return res
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])


@users.delete('/{user_id}', summary='Delete user')
async def delete_user(user_id: int) -> dict:
    res = await UsersService().delete_user(user_id=user_id)

    if res['status'] == 200:
        return res
    elif res['status'] == 404:
        raise HTTPException(status_code=404, detail=res['detail'])

    raise HTTPException(status_code=500, detail=res['detail'])


