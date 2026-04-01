import asyncio
from io import BytesIO
from app.ingest import ingest_file


def test_ingest_mock():
    result = asyncio.run(ingest_file(b"Hello world from sample document.", filename="sample.txt"))
    assert "answer" in result
    assert "citations" in result
    assert result["citations"][0]["source"] == "sample.txt"


def test_ingest_pdf():
    try:
        from reportlab.pdfgen import canvas
    except Exception:
        import pytest
        pytest.skip("reportlab not installed; skipping PDF test")

    # create a simple PDF in memory
    buf = BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(72, 720, "Hello PDF world")
    c.showPage()
    c.save()
    pdf_bytes = buf.getvalue()
    buf.close()

    result = asyncio.run(ingest_file(pdf_bytes, filename="sample.pdf"))
    assert "answer" in result
    assert "citations" in result
    assert result["citations"][0]["source"] == "sample.pdf"
    assert "Hello PDF world" in result["citations"][0]["snippet"]
