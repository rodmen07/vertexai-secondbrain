from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingest import ingest_file
from app.agent import router as agent_router
from app.drive_connector import DriveConnector

app = FastAPI(title="vertexai-secondbrain - Phase A scaffold")


class DriveIngestRequest(BaseModel):
    file_id: str
    filename: str = "drive_file"


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    result = await ingest_file(content, filename=file.filename)
    return result


@app.post("/ingest/drive")
async def ingest_drive(req: DriveIngestRequest):
    """Download a file from Google Drive by ID and ingest it."""
    connector = DriveConnector.from_env()
    try:
        content = connector.download_file(req.file_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Drive download failed: {e}")
    result = await ingest_file(content, filename=req.filename)
    result["source"] = "drive"
    result["file_id"] = req.file_id
    return result


# Agent routes
app.include_router(agent_router, prefix="/agent")
