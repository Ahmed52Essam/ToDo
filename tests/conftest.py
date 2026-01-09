import os
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.security import create_access_token
from app.db.base import Base, User
from app.db.session import get_db
from app.main import app

# Use the test database URL from config
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://myuser:mypassword@localhost:5432/todo_test_db",
)

# Create a specific engine for tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    # REMOVED: connect_args={"check_same_thread": False} (This is only for SQLite)
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module", autouse=True)
async def init_db():
    """Initialize the database once per test module."""
    # Create the test database tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Cleanup after module tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture that returns a SQLAlchemy session with a SAVEPOINT.
    This enables rollback after each test, keeping the DB clean.
    """
    async with test_engine.connect() as connection:
        # 1. Start the "Outer" Transaction (The Sandbox)
        transaction = await connection.begin()

        # 2. Bind the session to this connection
        async_session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )
        # 3. Start the "Inner" Transaction (The Savepoint)
        await async_session.begin_nested()

        # 4. The "Restarter" - This is the magic part!
        # If the app calls commit(), this event listener immediately
        # starts a NEW nested transaction so the session is never "naked".
        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def restart_savepoint(async_session, transaction):
            if transaction.nested and not transaction._parent.nested:
                async_session.begin_nested()

        yield async_session

        await async_session.close()

        # 5. Cleanup: Close session and Rollback the Outer Transaction
        await transaction.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture for the HTTP client that overrides the get_db dependency.
    """

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(db_session: AsyncSession) -> dict:
    async def _create_headers(email: str = "test@example.com") -> dict:
        # 1. Check if the user already exists
        stmt = select(User).where(User.email == email)
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        # 2. If they don't exist, create them
        if not user:
            user = User()
            user.email = email
            user.hashed_password = "passwordexample1234"
            db_session.add(user)

            await db_session.commit()
            await db_session.refresh(user)

        # 3. Create the token
        access_token = create_access_token(email=email)
        return {"Authorization": f"Bearer {access_token}"}

    return _create_headers
