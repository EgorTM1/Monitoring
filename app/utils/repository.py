from sqlalchemy import select, update, delete

from app.db import session_factory
from app.core import get_logger


logger = get_logger('app.utils.repository')

class Repository:
    model = None

    async def get_all(self, limit: int = 50) -> dict:
        async with session_factory() as session:
            try:
                query = select(self.model).limit(limit)

                result = await session.execute(query)
                res = result.scalars().all()

                logger.debug(f'GET ALL: {self.model.__name__} length: {len(res)}')

                return {'status': 200, 'detail': res}
                
            except Exception as e:
                logger.error(f'GET ALL: {self.model.__name__} error: {str(e)}')

                return {'status': 500, 'detail': f'error: {str(e)}'}


    async def create_one(self, create_obj: dict) -> dict:
        async with session_factory() as session:
            try:
                model_obj = self.model(**create_obj)

                session.add(model_obj)
                await session.flush()
                await session.commit()

                logger.info(f'CREATE: {self.model.__name__} id: {model_obj.id}')

                return {'status': 201, 'detail': f'success create. id: {model_obj.id}'}

            except Exception as e:
                logger.error(f'CREATE: {self.model.__name__} error: {str(e)}')

                await session.rollback()
                return {'status': 500, 'detail': f'error: {str(e)}'}


    async def get_by_id(self, obj_id: int) -> dict:
        async with session_factory() as session:
            try:
                obj = await session.get(self.model, obj_id)

                if not obj:
                    logger.warning(f'GET BY ID: {self.model.__name__} id: {obj_id} not found')

                    return {'status': 404, 'detail': 'Not found'}
                

                logger.debug(f'GET BY ID: {self.model.__name__} id: {obj_id}')

                return {'status': 200, 'detail': obj}

            except Exception as e:
                logger.error(f'GET BY ID: {self.model.__name__} id: {obj_id} error: {str(e)}')

                return {'status': 500, 'detail': f'error: {str(e)}'}


    async def update_one(self, upd_data: dict, upd_id: int) -> dict:
        async with session_factory() as session:
            try:
                obj = await session.get(self.model, upd_id)

                if not obj:
                    logger.warning(f'UPDATE: {self.model.__name__} id: {upd_id} not found')

                    return {'status': 404, 'detail': 'Not found'}

                upd_data = {key: value for key, value in upd_data.items() if value is not None}
                stmt = update(self.model).values(upd_data).where(self.model.id == upd_id)

                await session.execute(stmt)
                await session.commit()

                logger.info(f'UPDATE: {self.model.__name__} id: {upd_id}')

                return {'status': 200, 'detail': f'success update'}

            except Exception as e:
                logger.error(f'UPDATE: {self.model.__name__} id: {upd_id} error: {str(e)}')

                await session.rollback()
                return {'status': 500, 'detail': f'error: {str(e)}'}


    async def delete_one(self, obj_id: int) -> dict:
        async with session_factory() as session:
            try:
                obj = await session.get(self.model, obj_id)
                
                if not obj:
                    logger.warning(f'DELETE: {self.model.__name__} id: {obj_id} not found')

                    return {'status': 404, 'detail': 'Not found'}

                stmt = delete(self.model).where(self.model.id == obj_id)

                await session.execute(stmt)
                await session.commit()

                logger.info(f'DELETE: {self.model.__name__} id: {obj_id}')

                return {'status': 200, 'detail': f'success delete'}

            except Exception as e:
                logger.error(f'DELETE: {self.model.__name__} id: {obj_id} error: {str(e)}')

                await session.rollback()
                return {'status': 500, 'detail': f'error: {str(e)}'}
