from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_mock():
    resp = client.post("/ingest", files={"file": ("sample.txt", b"Hello world from sample document.", "text/plain")})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "citations" in data
    assert data["citations"][0]["source"] == "sample.txt"
