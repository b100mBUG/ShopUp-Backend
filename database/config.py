from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(url=DATABASE_URL, echo=False)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

CLOUDINARY_API_SECRET = "9m9V70fjzCeqzhPWT7YQtNhBKgY"
CLOUDINARY_API_KEY = 124212226626295
CLOUDINARY_CLOUD_NAME = "dmebkwyew"