import pytest

from app import make_app


@pytest.fixture(autouse=True, scope="session")
def session(worker_id):
    yield type("", (), {"worker_id": worker_id})


@pytest.fixture(autouse=True)
def tst(session):
    application = make_app()
    session.client = application.test_client()
    with application.app_context():
        yield session
