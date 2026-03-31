import asyncio
from typing import Any, Dict

async def ingest_file(content: bytes, filename: str = "uploaded") -> Dict[str, Any]:
    """Mock ingest that extracts text from uploaded bytes and returns a cited answer.
    Replace with real PDF parsing and RAG pipeline later.
    """
    # naive decoding; real implementation should use PDF parsing libraries
    text = content.decode('utf-8', errors='ignore')
    # simulate async processing
    await asyncio.sleep(0)
    answer = f"Mocked summary for {filename}"
    citations = [{"source": filename, "snippet": text[:200]}]
    return {"answer": answer, "citations": citations}
