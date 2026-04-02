from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_agent_init_and_query():
    r = client.post("/agent/init", json={"name": "test"})
    assert r.status_code == 200
    body = r.json()
    assert "agent_id" in body

    r2 = client.post("/agent/query", json={"agent_id": body["agent_id"], "prompt": "hello"})
    assert r2.status_code == 200
    assert "answer" in r2.json()
