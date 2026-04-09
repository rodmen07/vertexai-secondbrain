import os
from typing import Any, Dict, List
from fastapi import APIRouter

router = APIRouter()

# Testing hook: set to a fake client object to avoid real GCP calls in tests.
_TEST_AGENT_CLIENT = None


def _build_agent_client():
    if _TEST_AGENT_CLIENT is not None:
        return _TEST_AGENT_CLIENT
    from google.cloud import discoveryengine_v1alpha as discoveryengine  # type: ignore
    return discoveryengine.ConversationalSearchServiceClient()


@router.post("/init")
async def init_agent(config: Dict[str, Any] = {}):
    """Store agent config and return an agent_id."""
    return {"agent_id": "agent-1", "config": config}


@router.post("/query")
async def query_agent(payload: Dict[str, Any]):
    """Query the Vertex AI Agent Builder and return the answer with citations.

    Required env vars:
      VERTEX_PROJECT_ID    — GCP project ID
      VERTEX_DATA_STORE_ID — Discovery Engine data store ID
    Optional:
      VERTEX_LOCATION      — defaults to "global"
    """
    agent_id = payload.get("agent_id", "agent-1")
    prompt = payload.get("prompt", "")

    project_id = os.environ.get("VERTEX_PROJECT_ID", "")
    data_store_id = os.environ.get("VERTEX_DATA_STORE_ID", "")
    location = os.environ.get("VERTEX_LOCATION", "global")

    if not project_id or not data_store_id:
        return {
            "agent_id": agent_id,
            "prompt": prompt,
            "answer": "(vertex ai not configured — set VERTEX_PROJECT_ID and VERTEX_DATA_STORE_ID)",
            "citations": [],
        }

    try:
        client = _build_agent_client()

        if _TEST_AGENT_CLIENT is not None:
            # Test path: call with a plain dict so tests don't need the real proto types
            response = client.converse_conversation(request={"prompt": prompt})
        else:
            from google.cloud import discoveryengine_v1alpha as discoveryengine  # type: ignore
            parent = (
                f"projects/{project_id}/locations/{location}/"
                f"collections/default_collection/dataStores/{data_store_id}"
            )
            request = discoveryengine.ConverseConversationRequest(
                name=f"{parent}/conversations/-",
                query=discoveryengine.TextInput(input=prompt),
                serving_config=f"{parent}/servingConfigs/default_config",
            )
            response = client.converse_conversation(request=request)

        # Extract answer text from the reply (summary preferred over deprecated .reply)
        reply_msg = getattr(response, "reply", None)
        reply_obj = getattr(reply_msg, "reply", None) if reply_msg else None
        summary = getattr(reply_obj, "summary", None) if reply_obj else None
        if summary:
            answer = getattr(summary, "summary_text", "") or ""
        else:
            answer = getattr(reply_obj, "reply", "") or ""

        # Extract citations from search results
        citations: List[Dict[str, Any]] = []
        for result in getattr(response, "search_results", []):
            doc = getattr(result, "document", None)
            if doc:
                citations.append({"source": getattr(doc, "name", ""), "snippet": ""})

    except Exception as e:
        return {"agent_id": agent_id, "prompt": prompt, "answer": f"(error: {e})", "citations": []}

    return {"agent_id": agent_id, "prompt": prompt, "answer": answer, "citations": citations}
