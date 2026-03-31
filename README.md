vertexai-secondbrain — Phase A scaffold

This repository contains a minimal Phase A scaffold for the Vertex AI "Second Brain" portfolio exercise.

What is included:
- FastAPI service stub (app/) exposing an /ingest endpoint that accepts an uploaded file and returns a mocked cited answer.
- Simple ingest mock implementing text extraction and citation formatting.
- Pytest test exercising the ingest endpoint.
- Terraform/placeholder for IaC (terraform/).

How to run (local development):

1. python -m venv .venv
2. .\.venv\Scripts\Activate.ps1  # Windows PowerShell
3. pip install -r requirements.txt
4. uvicorn app.main:app --reload --port 8081

API:
POST /ingest - multipart/form-data file upload. Returns { answer: string, citations: [{source, snippet}] }

Notes:
- This is a Phase A scaffold: mocked extraction + citation. Replace ingest mock with real PDF parsing and RAG flow when ready.
- Keep agent instructions domain-agnostic and store session memory in Firestore (Phase B).
