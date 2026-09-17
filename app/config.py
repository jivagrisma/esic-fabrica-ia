import os

PROJECT_ID = os.environ.get("PROJECT_ID", "esic-fabrica-ia")
PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER", "985215895070")
VERTEX_REGION = os.environ.get("VERTEX_REGION", "us-central1")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Document AI opera en la región multi-región "us" de este proyecto
# (decisión documentada en docs/01-arquitectura-solucion.md).
DOCAI_LOCATION = os.environ.get("DOCAI_LOCATION", "us")
DOCAI_PROCESSOR = os.environ.get(
    "DOCAI_PROCESSOR",
    f"projects/{PROJECT_NUMBER}/locations/{DOCAI_LOCATION}/processors/33966db067a8aeba",
)
DOCAI_ENDPOINT = f"{DOCAI_LOCATION}-documentai.googleapis.com"
