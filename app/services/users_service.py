from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.utils import Repository
from app.models import UsersOrm
from app.db import session_factory
from app.schemas import UserAdd, UserGetDTO, UserUpdate


class UsersService(Repository):
    model = UsersOrm

    async def get_all(self, limit: int = 50) -> dict:
        res = await super().get_all(limit)

        return res


    async def add_user(self, user: UserAdd) -> dict:
        user_dict = user.model_dump()

        res = await super().create_one(user_dict)

        return res


    async def get_user_by_id(self, user_id: int) -> dict:
        res = await super().get_by_id(user_id)

        return res


    async def update_user(self, upd_data: UserUpdate, user_id: int) -> dict:
        upd_data_dict = upd_data.model_dump()

        res = await super().update_one(upd_data_dict, user_id)

        return res


    async def delete_user(self, user_id: int) -> dict:
        res = await super().delete_one(user_id)

        return res


    async def get_all_with_rel(self) -> dict:
        async with session_factory() as session:
            try:
                query = (
                    select(self.model)
                    .options(selectinload(self.model.posts))
                    .options(selectinload(self.model.comments))
                )

                result = await session.execute(query)
                res = result.scalars().all()

                return {'status': 200, 'detail': res}

            except Exception as e:
                await session.rollback()
                return {'status': 500, 'detail': f'error: {str(e)}'}

