import pytest
from app import app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def runner():
    return app.test_cli_runner()


def test_get(client):
    response = client.get("/")
    assert b"<p>Hello from archiver!</p>" in response.data
