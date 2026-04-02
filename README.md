# vertexai-secondbrain

FastAPI-based Phase A prototype for a document-grounded "Second Brain" portfolio build on GCP and Vertex AI patterns.

## Current state

Implemented in this repo today:

- `POST /ingest` reads uploaded files and extracts text from PDFs with `pypdf`, with plain-text fallback for non-PDF input.
- Citation-shaped responses are returned from ingest so downstream RAG wiring has a stable response contract.
- `POST /agent/init` and `POST /agent/query` provide a minimal agent scaffold for later Vertex AI integration.
- `app/drive_connector.py` contains a small Google Drive wrapper for listing files and downloading content.
- Unit tests cover ingest, the agent scaffold, and the Drive connector.

Not implemented yet:

- Vertex AI Agent Builder wiring
- Drive connector authentication flow and endpoint integration
- Web grounding
- Firestore-backed session memory
- Gmail connector and external extension work

## Project layout

- `app/main.py` - FastAPI app with `/health`, `/ingest`, and `/agent/*` routes
- `app/ingest.py` - PDF/text extraction and citation response shaping
- `app/agent.py` - minimal agent initialization and query handlers
- `app/drive_connector.py` - Google Drive listing and download helper
- `tests/` - unit tests for ingest, agent scaffold, and Drive connector
- `terraform/` - IaC placeholder for later deployment work

## Local development

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8081
```

### Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8081
```

## API surface

- `GET /health` - basic health check
- `POST /ingest` - multipart upload, returns `{answer, citations}`
- `POST /agent/init` - returns a placeholder `agent_id`
- `POST /agent/query` - echoes prompt metadata and returns a placeholder answer

## Notes

- This is still a local scaffold, not a full Vertex AI deployment.
- The Drive connector is intentionally small and testable; it is not yet connected to FastAPI routes or Agent Builder.
- The next meaningful milestone is wiring Drive ingestion into the agent flow and enabling web grounding.
