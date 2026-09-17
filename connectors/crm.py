"""Conector SIMULADO al CRM institucional (p. ej. Microsoft Dynamics 365).

CONTRATO REAL (documentación, NO implementado):
  POST https://crm.esic.edu/api/v1/tickets
  Headers: Authorization: Bearer <OAuth2 del tenant ESIC>
  Body:    {"contact_id": "...", "category": "admisiones|financiero|academico",
            "priority": "normal|alta", "summary": "...", "transcript": [...]}
  Respuesta esperada: 201 {"ticket_id": "CRM-1234", "owner": "agente@esic.edu"}

En el MVP: genera el mismo payload y devuelve un ticket simulado determinista.
"""

_PREFIX = "CRM"


def create_ticket(payload: dict) -> dict:
    ticket_id = f"{_PREFIX}-{abs(hash(payload.get('summary', ''))) % 9000 + 1000}"
    return {
        "simulated": True,
        "endpoint_documentado": "POST https://crm.esic.edu/api/v1/tickets",
        "payload_enviado": payload,
        "ticket_id": ticket_id,
        "owner": "agente.admisiones@esic.demo (simulado)",
        "mensaje": (
            "Ticket creado en CRM SIMULADO. En producción, este payload se enviaría "
            "al CRM real vía OAuth2 y el agente humano recibiría la transcripción completa."
        ),
    }
