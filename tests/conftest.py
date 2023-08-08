import pytest
from fastapi.testclient import TestClient
from redis import asyncio

from app.db.database import Base, SessionLocal, engine, get_db
from app.main import app


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True, scope="session")
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture(autouse=True, scope="session")
async def delete_cache():
    redis = asyncio.from_url(
        "redis://localhost",
        encoding="utf8",
        decode_responses=True,
    )
    await redis.flushall()
    yield None
    await redis.flushall()
