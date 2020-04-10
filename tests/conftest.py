import pytest
from app import make_app
from common_database.mongodb import db, get_client

_connection = None


@pytest.fixture(autouse=True, scope="session")
def session(worker_id):
    yield type("", (), {"worker_id": worker_id})


@pytest.fixture(autouse=True)
def tst(session):
    application = make_app()
    session.client = application.test_client()
    database = db(application.config["SERVICE_DB"])
    session.db = database
    with application.app_context():
        yield session
    get_client().drop_database(application.config["SERVICE_DB"])
