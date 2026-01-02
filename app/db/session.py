from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import config

# 2. Create the Async Engine
engine = create_async_engine(
    config.DATABASE_URL,
    echo=True,  # Log SQL queries to console (useful for debugging)
)

# 3. Create the Session Factory
# This is what we use to create new sessions for each request
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Important for async to prevent implicit IO
)


# 5. Dependency for FastAPI
# This function is injected into your routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
