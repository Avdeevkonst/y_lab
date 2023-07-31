import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:avdeev97@localhost/ylab"

engine_test = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine_test)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine_test)
