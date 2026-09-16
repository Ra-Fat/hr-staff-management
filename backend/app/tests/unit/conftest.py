# import pytest_asyncio
# from httpx import AsyncClient, ASGITransport
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# import asyncio
# import pytest

# from app.main import app
# from app.core.config import settings
# from app.core.database import Base, get_db
# from app.domain.admin_user.model import AdminUser
# from app.core.utils import hash_password

# API = "/api"

# engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)

# @pytest.fixture(scope="session")
# def event_loop():
#     """Force a single event loop for the whole test session.

#     Required for pytest-asyncio < 0.24 so our session-scoped engine
#     (asyncpg connection pool) doesn't get bound to a dead loop between tests.
#     """
#     policy = asyncio.get_event_loop_policy()
#     loop = policy.new_event_loop()
#     yield loop
#     loop.close()


# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     await engine.dispose()


# @pytest_asyncio.fixture
# async def db_session():
#     connection = await engine.connect()
#     transaction = await connection.begin()
#     session = AsyncSession(
#         bind=connection,
#         expire_on_commit=False,
#         join_transaction_mode="create_savepoint",
#     )
#     try:
#         yield session
#     finally:
#         await session.rollback()
#         await session.close()
#         await transaction.rollback()
#         await connection.close()


# @pytest_asyncio.fixture
# async def client(db_session):
#     async def override_get_db():
#         yield db_session

#     app.dependency_overrides[get_db] = override_get_db
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         yield ac
#     app.dependency_overrides.clear()


# @pytest_asyncio.fixture
# async def admin_token(client, db_session):
#     from app.domain.role.model import Role

#     role = Role(name="Super Admin")
#     db_session.add(role)
#     await db_session.flush()
#     await db_session.refresh(role)

#     admin = AdminUser(
#         full_name="Test Admin",
#         email="test-admin@example.com",
#         password_hash=hash_password("TestPass123!"),
#         role_id=role.id,
#         status="ACTIVE"
#     )
#     db_session.add(admin)
#     await db_session.flush()
#     await db_session.refresh(admin)

#     login_res = await client.post(f"{API}/auths/auth/login", json={
#         "email": "test-admin@example.com",
#         "password": "TestPass123!",
#     })
#     assert login_res.status_code == 200, login_res.text
#     return login_res.json()["data"]["access_token"]