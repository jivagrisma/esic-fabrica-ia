"""Escenario 1: chatbot de consultas con grounding en la KB institucional."""
import json

from google.cloud import firestore

from app.gcp import db, gemini_generate
from app.kb import CONTACTO_HUMANO, EMPLEO, FINANCIAMIENTO, PROGRAMAS
from connectors.crm import create_ticket

SYSTEM_PROMPT = """Eres "ESIC Assistant", el asistente virtual oficial de ESIC Medellín.

Reglas estrictas:
1. Responde ÚNICAMENTE con la información de la base de conocimiento entregada. Te está PROHIBIDO inventar datos, precios, fechas o políticas.
2. Deriva a un agente humano (derivar=true) cuando: el usuario presente una queja o reclamo; el caso financiero personal sea complejo (moras, acuerdos de pago, apelaciones de beca); la consulta no tenga respuesta en la base de conocimiento; o el usuario pida expresamente hablar con una persona.
3. Si la consulta está fuera del dominio institucional (temas no relacionados con ESIC), declina amablemente, ofrece derivación y no respondas el tema ajeno.
4. Respuestas en español, máximo ~120 palabras, tono institucional cálido y cercano.

Debes responder SIEMPRE en JSON con esta forma exacta:
{"respuesta": str, "derivar": bool, "categoria": "admisiones|financiero|academico|empleo|otro", "resumen": str}
"resumen" es un resumen breve del caso para el agente humano."""

_VALID_CATEGORIES = {"admisiones", "financiero", "academico", "empleo", "otro"}
_CATEGORIA_CONTACTO = {"admisiones": "admisiones", "financiero": "financiero"}


def _kb_serializada() -> str:
    return json.dumps(
        {
            "programas": PROGRAMAS,
            "financiamiento": FINANCIAMIENTO,
            "empleo": EMPLEO,
            "contacto_humano": CONTACTO_HUMANO,
        },
        ensure_ascii=False,
        indent=2,
    )


def _parsear_respuesta(raw: str) -> dict:
    try:
        data = json.loads(raw)
        return {
            "respuesta": str(data.get("respuesta", "")).strip(),
            "derivar": bool(data.get("derivar", False)),
            "categoria": data.get("categoria") if data.get("categoria") in _VALID_CATEGORIES else "otro",
            "resumen": str(data.get("resumen", ""))[:500],
        }
    except (json.JSONDecodeError, AttributeError, TypeError):
        return {
            "respuesta": raw.strip() or "Lo siento, hubo un problema. ¿Puedes repetir tu consulta?",
            "derivar": False,
            "categoria": "otro",
            "resumen": "",
        }


def handle_chat(message: str, session_id: str) -> dict:
    """Atiende una consulta del chat: responde con Gemini + KB, deriva y persiste."""
    prompt = (
        f"BASE DE CONOCIMIENTO ESIC:\n{_kb_serializada()}\n\n"
        f"MENSAJE DEL USUARIO:\n{message}\n\n"
        "Responde en el JSON indicado."
    )
    raw = gemini_generate(prompt, system_instruction=SYSTEM_PROMPT, json_mode=True)
    parsed = _parsear_respuesta(raw)

    reply = parsed["respuesta"]
    escalated = parsed["derivar"]
    categoria = parsed["categoria"]
    ticket = None

    if escalated:
        payload = {
            "contact_id": session_id,
            "category": categoria,
            "priority": "normal",
            "summary": parsed["resumen"] or message[:200],
            "transcript": [{"role": "user", "text": message}],
        }
        ticket = create_ticket(payload)
        contacto = CONTACTO_HUMANO.get(
            _CATEGORIA_CONTACTO.get(categoria, ""), CONTACTO_HUMANO["admisiones"]
        )
        reply = (
            f"{reply}\n\nTe derivé a un agente humano. Tu ticket es "
            f"{ticket['ticket_id']}. Contacto directo: {contacto}."
        )

    interaction_id = "no-registrado"
    try:
        ref = db().collection("interactions").add({
            "session_id": session_id,
            "message": message,
            "reply": reply,
            "escalated": escalated,
            "categoria": categoria,
            "ts": firestore.SERVER_TIMESTAMP,
            "model": "gemini-2.5-flash",
        })
        interaction_id = ref[1].id
        if ticket is not None:
            db().collection("tickets").add({**ticket, "session_id": session_id})
    except Exception:
        pass

    return {
        "reply": reply,
        "escalated": escalated,
        "ticket": ticket,
        "interaction_id": interaction_id,
    }
