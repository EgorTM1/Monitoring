from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.settings import settings


engine = create_async_engine(
    url=settings.get_dsn,
    echo=False
)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
