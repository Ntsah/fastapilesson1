from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'eminem'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DB_NAME = 'ecommerce'


engine = create_async_engine(
    f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}',
    echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
