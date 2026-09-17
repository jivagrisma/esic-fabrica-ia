"""Clientes GCP compartidos: Vertex AI (Gemini), Document AI y Firestore.

Autenticación 100% por Application Default Credentials (ADC): en Cloud Run usa
la service account del runtime; en local, `gcloud auth application-default login`.
Cero claves en el código o el repo.
"""
import functools

import vertexai
from google.cloud import documentai, firestore
from vertexai.generative_models import GenerativeModel

from app.config import (
    DOCAI_ENDPOINT,
    DOCAI_PROCESSOR,
    GEMINI_MODEL,
    PROJECT_ID,
    VERTEX_REGION,
)


@functools.lru_cache(maxsize=1)
def _vertex():
    vertexai.init(project=PROJECT_ID, location=VERTEX_REGION)
    return True


@functools.lru_cache(maxsize=8)
def _model(system_instruction: str | None) -> GenerativeModel:
    _vertex()
    return GenerativeModel(GEMINI_MODEL, system_instruction=system_instruction)


def gemini_generate(
    prompt: str, *, system_instruction: str | None = None, json_mode: bool = False
) -> str:
    """Llama a Gemini en Vertex AI y devuelve el texto de la respuesta.

    Nota: el ID de modelo no se verificó contra la API en vivo (ver
    docs/01-arquitectura-solucion.md); es configurable vía GEMINI_MODEL.
    """
    model = _model(system_instruction)
    kwargs = {}
    if json_mode:
        kwargs["generation_config"] = {"response_mime_type": "application/json"}
    response = model.generate_content(prompt, **kwargs)
    try:
        return response.text or ""
    except ValueError:
        return ""


@functools.lru_cache(maxsize=1)
def docai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": DOCAI_ENDPOINT}
    )


def docai_process(content: bytes, mime_type: str) -> documentai.Document:
    """OCR + extracción vía Document AI (processor configurado en config.py)."""
    client = docai_client()
    request = documentai.ProcessRequest(
        name=DOCAI_PROCESSOR,
        raw_document=documentai.RawDocument(content=content, mime_type=mime_type),
    )
    result = client.process_document(request=request)
    return result.document


@functools.lru_cache(maxsize=1)
def db() -> firestore.Client:
    return firestore.Client(project=PROJECT_ID)
