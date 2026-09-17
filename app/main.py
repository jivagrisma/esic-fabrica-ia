"""ESIC Fábrica de IA — Micro-MVP (FastAPI sobre Cloud Run).

Contratos de módulos (implementados por escenario):
  - app.scenario1_chat.handle_chat(message: str, session_id: str) -> dict
  - app.scenario2_docs.handle_document(file_bytes, mime_type, doc_type, applicant) -> dict

Los endpoints son síncronos (`def`): FastAPI los ejecuta en threadpool, lo que
permite usar los SDKs de Google (bloqueantes) sin bloquear el event loop.
"""
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.scenario1_chat import handle_chat
from app.scenario2_docs import handle_document

app = FastAPI(title="ESIC Fábrica de IA — Micro-MVP", version="1.0.0")

STATIC = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat")
def chat_endpoint(payload: dict):
    message = (payload or {}).get("message", "").strip()
    session_id = (payload or {}).get("session_id", "anon")
    if not message:
        raise HTTPException(status_code=400, detail="message es obligatorio")
    try:
        result = handle_chat(message, session_id)
        return JSONResponse(result)
    except Exception as exc:  # noqa: BLE001 — el MVP reporta el error tal cual
        raise HTTPException(status_code=500, detail=f"error_chat: {exc}") from exc


@app.post("/api/documents")
async def documents_endpoint(
    file: UploadFile = File(...),
    doc_type: str = Form("cedula"),
    applicant_name: str = Form(""),
    solicitud_id: str = Form("SOL-0001"),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="archivo vacío")
    try:
        result = handle_document(
            content, file.content_type or "application/pdf", doc_type,
            {"nombre": applicant_name, "solicitud_id": solicitud_id},
        )
        return JSONResponse(result)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"error_documento: {exc}") from exc
