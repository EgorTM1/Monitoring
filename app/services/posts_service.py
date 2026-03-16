from sqlalchemy import select

from app.utils import Repository
from app.models import PostsOrm
from app.db import session_factory

from app.schemas import PostAdd, PostGet, PostUpdate


class PostsService(Repository):
    model = PostsOrm

    async def add_post(self, post: PostAdd) -> dict:
        post_dict = post.model_dump()

        res = await super().create_one(post_dict)

        return res

    async def get_all(self, limit: int = 50) -> dict:
        res = await super().get_all(limit)

        return res

    async def get_post_by_id(self, post_id: int) -> dict:
        res = await super().get_by_id(post_id)

        return res

    async def get_posts_at_user(self, user_id: int) -> dict:
        async with session_factory() as session:
            try:
                query = select(self.model).where(self.model.user_id == user_id)

                result = await session.execute(query)
                res = result.scalars().all()

                return {'status': 200, 'detail': res}

            except Exception as e:
                await session.rollback()
                return {'status': 500, 'detail': f'error: {str(e)}'}

    async def update_post(self, post: PostUpdate, post_id: int) -> dict:
        post_dict = post.model_dump()

        res = await super().update_one(post_dict, post_id)

        return res

    async def delete_post(self, post_id: int) -> dict:
        res = await super().delete_one(post_id)

        return res
        