import pytest
import json
from zipfile import ZipFile
from pathlib import Path

from app import app
from archive_processor.unpacker import get_zip_content


# Test are performed on in-memory sqlite database which name defined in tests/__init__.py
@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def runner():
    return app.test_cli_runner()


def test_get(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_zip_content():
    expected = [{'path': 'new_file_1', 'size': 11}]
    assert get_zip_content(ZipFile('tests/static/test_archive.zip')) == expected


def test_upload_file(client):
    static = Path(__file__).parent / "static"
    response = client.post("/", data={
        "file": (static / 'test_archive.zip').open("rb"),
    })
    assert response.status_code == 200
    expected = {'content': [{'path': 'new_file_1', 'size': 11}],
                'file': 'test_archive.zip',
                'id': 1}
    assert json.loads(response.data) == expected
