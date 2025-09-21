from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://fidelcastro:NXFDa7exbwGbUHQ8JrUuVwHTNTvkHtCB@dpg-d37njbjuibrs7396lq00-a.render.com/shop_up_database"

engine = create_async_engine(url=DATABASE_URL, echo=False)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

CLOUDINARY_API_SECRET = "9m9V70fjzCeqzhPWT7YQtNhBKgY"
CLOUDINARY_API_KEY = 124212226626295

CLOUDINARY_CLOUD_NAME = "dmebkwyew"
