"""Conector SIMULADO a Microsoft 365 (Graph API) — notificaciones al equipo interno.

CONTRATO REAL (documentación, NO implementado):
  POST https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages
  Headers: Authorization: Bearer <Azure AD app-only token>
  Body:    {"body": {"contentType": "html", "content": "...resumen de la alerta..."}}

En el MVP: devuelve la confirmación simulada con el mensaje que se publicaría.
"""


def notificar_alerta_ms_teams(resumen: str) -> dict:
    return {
        "simulated": True,
        "endpoint_documentado": "POST https://graph.microsoft.com/v1.0/teams/{id}/channels/{id}/messages",
        "mensaje_publicado": resumen,
        "mensaje": "Alerta publicada en Microsoft Teams SIMULADA.",
    }
