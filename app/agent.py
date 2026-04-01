from typing import Any, Dict
from fastapi import APIRouter

router = APIRouter()


@router.post("/init")
async def init_agent(config: Dict[str, Any] = {}):
    """Minimal agent initializer (placeholder).

    Returns an agent id and echoes the provided config. Replace with
    Vertex AI Agent bootstrap logic in Phase A implementation.
    """
    return {"agent_id": "agent-1", "config": config}


@router.post("/query")
async def query_agent(payload: Dict[str, Any]):
    """Minimal query endpoint for the scaffold agent.

    Expects JSON: {"agent_id": "...", "prompt": "..."}
    """
    agent_id = payload.get("agent_id", "agent-1")
    prompt = payload.get("prompt", "")
    # Placeholder response — replace with RAG/Agent logic later
    return {"agent_id": agent_id, "prompt": prompt, "answer": "(placeholder)"}
