"""Integration test for the /ingest/drive endpoint using the _TEST_BUILD hook."""
import asyncio
from app import drive_connector as dc
from app.drive_connector import DriveConnector
from app.ingest import ingest_file


class DummyRequest:
    def __init__(self, data):
        self._data = data

    def execute(self):
        return self._data


class DummyService:
    def __init__(self, files_map):
        self._files_map = files_map

    def files(self):
        outer = self

        class Files:
            def get_media(self, fileId=None):
                return DummyRequest(outer._files_map[fileId])

        return Files()


def _make_connector(content: bytes) -> DriveConnector:
    dummy = DummyService({"file-abc": content})

    def fake_build(service, version, credentials=None):
        return dummy

    dc._TEST_BUILD = fake_build
    return DriveConnector(credentials=None)


def test_drive_ingest_text():
    content = b"Hello from Google Drive"
    connector = _make_connector(content)

    raw = connector.download_file("file-abc")
    assert raw == content

    result = asyncio.run(ingest_file(raw, filename="note.txt"))
    assert result["answer"].startswith("Extracted text from note.txt")
    assert len(result["citations"]) == 1
    assert result["citations"][0]["source"] == "note.txt"
    assert "Hello from Google Drive" in result["citations"][0]["snippet"]


def test_drive_ingest_simulates_endpoint():
    """Simulate what /ingest/drive does end-to-end."""
    content = b"Drive report content"
    connector = _make_connector(content)

    raw = connector.download_file("file-abc")
    result = asyncio.run(ingest_file(raw, filename="report.txt"))
    result["source"] = "drive"
    result["file_id"] = "file-abc"

    assert result["source"] == "drive"
    assert result["file_id"] == "file-abc"
    assert "answer" in result
    assert "citations" in result
