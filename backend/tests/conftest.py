import os

os.environ["DATABASE_URL"] = "sqlite:///./test_gv_diagnostics.db"
os.environ["FRONTEND_URL"] = "http://testserver"

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def pytest_sessionfinish(session, exitstatus):
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)
