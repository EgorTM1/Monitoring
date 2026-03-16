from sqlalchemy import select

from app.models import CommentsOrm
from app.utils import Repository
from app.db import session_factory

from app.schemas import CommentAdd, CommentUpdate


class CommentsService(Repository):
    model = CommentsOrm

    async def add_comment(self, comment: CommentAdd) -> dict:
        comment_dict = comment.model_dump()

        res = await super().create_one(comment_dict)

        return res

    async def get_comments_at_post(self, post_id: int) -> dict:
        async with session_factory() as session:
            try:
                query = (
                    select(self.model)
                    .where(self.model.post_id == post_id) 
                )

                result = await session.execute(query)
                res = result.scalars().all()

                return {'status': 200, 'detail': res}

            except Exception as e:
                await session.rollback()
                return {'status': 500, 'detail': f'error: {str(e)}'}

    async def get_comment_by_id(self, comment_id: int) -> dict:
        res = await super().get_by_id(comment_id)

        return res

    async def update_comment(self, comment: CommentUpdate, comment_id: int) -> dict:
        comment_dict = comment.model_dump()

        res = await super().update_one(comment_dict, comment_id)

        return res

    async def delete_comment(self, comment_id: int) -> dict:
        res = await super().delete_one(comment_id)

        return res