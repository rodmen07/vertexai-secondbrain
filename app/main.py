from fastapi import FastAPI, UploadFile, File
from app.ingest import ingest_file

app = FastAPI(title="vertexai-secondbrain - Phase A scaffold")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    result = await ingest_file(content, filename=file.filename)
    return result
