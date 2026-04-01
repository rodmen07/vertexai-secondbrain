import asyncio
from typing import Any, Dict
from io import BytesIO

def _extract_text_from_pdf(content: bytes) -> str:
    try:
        from pypdf import PdfReader
    except Exception:
        return ""
    try:
        reader = PdfReader(BytesIO(content))
    except Exception:
        return ""
    texts = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        texts.append(text)
    return "\n".join(texts)

async def ingest_file(content: bytes, filename: str = "uploaded") -> Dict[str, Any]:
    """Ingest that extracts text from uploaded bytes and returns a cited answer.
    Supports PDF (via pypdf) and plain text fallback.
    """
    text = ""
    is_pdf = False
    if isinstance(content, (bytes, bytearray)) and content[:4] == b"%PDF":
        is_pdf = True
    if filename.lower().endswith(".pdf"):
        is_pdf = True

    if is_pdf:
        text = _extract_text_from_pdf(content)
        if not text:
            # fallback to naive decode if PDF extraction failed
            text = content.decode("utf-8", errors="ignore")
    else:
        text = content.decode("utf-8", errors="ignore")

    await asyncio.sleep(0)
    answer = f"Extracted text from {filename} ({len(text)} chars)"
    citations = [{"source": filename, "snippet": text[:200]}]
    return {"answer": answer, "citations": citations}
