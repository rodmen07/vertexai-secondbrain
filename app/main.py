from fastapi import FastAPI, UploadFile, File
from app.ingest import ingest_file
from app.agent import router as agent_router

app = FastAPI(title="vertexai-secondbrain - Phase A scaffold")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    result = await ingest_file(content, filename=file.filename)
    return result


# Agent scaffold routes (Phase A placeholder)
app.include_router(agent_router, prefix="/agent")
