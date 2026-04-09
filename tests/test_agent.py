import asyncio
import os
import app.agent as agent_module
from app.agent import init_agent, query_agent


def test_agent_init():
    body = asyncio.run(init_agent({"name": "test"}))
    assert "agent_id" in body
    assert body["config"] == {"name": "test"}


def test_agent_query_not_configured():
    """With no env vars set, query should degrade gracefully (not crash)."""
    env_backup = {k: os.environ.pop(k, None) for k in ("VERTEX_PROJECT_ID", "VERTEX_DATA_STORE_ID")}
    try:
        resp = asyncio.run(query_agent({"agent_id": "agent-1", "prompt": "hello"}))
        assert "answer" in resp
        assert resp["answer"] != "(placeholder)"
        assert "citations" in resp
    finally:
        for k, v in env_backup.items():
            if v is not None:
                os.environ[k] = v


def test_agent_query_with_fake_client():
    """With a fake client injected, query should return the fake answer."""

    class FakeReplyObj:
        summary = None
        reply = "hello from vertex"

    class FakeReplyMsg:
        reply = FakeReplyObj()

    class FakeResponse:
        reply = FakeReplyMsg()
        search_results = []

    class FakeClient:
        def converse_conversation(self, request):
            return FakeResponse()

    original = agent_module._TEST_AGENT_CLIENT
    try:
        agent_module._TEST_AGENT_CLIENT = FakeClient()
        os.environ["VERTEX_PROJECT_ID"] = "test-project"
        os.environ["VERTEX_DATA_STORE_ID"] = "test-store"

        resp = asyncio.run(query_agent({"agent_id": "agent-1", "prompt": "hello"}))
        assert resp["answer"] == "hello from vertex"
        assert resp["citations"] == []
    finally:
        agent_module._TEST_AGENT_CLIENT = original
        os.environ.pop("VERTEX_PROJECT_ID", None)
        os.environ.pop("VERTEX_DATA_STORE_ID", None)
