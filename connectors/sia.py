"""Conector SIMULADO al sistema académico (SIA).

CONTRATO REAL (documentación, NO implementado):
  POST https://sia.esic.edu/api/v1/solicitudes/{id}/documentos
  Headers: Authorization: Bearer <service-to-service token>
  Body:    {"tipo": "cedula|transcript|certificado",
            "estado": "validado|alerta|rechazado",
            "campos_extraidos": {...}, "reporte_validacion_id": "..."}
  Respuesta esperada: 202 {"solicitud_estado": "en_admision", "recibo": "REC-77"}

En el MVP: valida el payload contra el esquema y devuelve la respuesta simulada.
"""

_CONTRACT = {
    "campos_obligatorios": ["tipo", "estado", "campos_extraidos", "reporte_validacion_id"],
    "estados_validos": ["validado", "alerta", "rechazado"],
}


def entregar_documento(payload: dict) -> dict:
    faltan = [c for c in _CONTRACT["campos_obligatorios"] if c not in payload]
    if faltan:
        return {"simulated": True, "ok": False, "error_contrato": f"faltan campos: {faltan}"}
    if payload["estado"] not in _CONTRACT["estados_validos"]:
        return {"simulated": True, "ok": False, "error_contrato": "estado inválido"}
    return {
        "simulated": True,
        "ok": True,
        "endpoint_documentado": f"POST https://sia.esic.edu/api/v1/solicitudes/{payload.get('solicitud_id','?')}/documentos",
        "payload_enviado": payload,
        "solicitud_estado": "en_admision",
        "recibo": f"REC-{abs(hash(payload['reporte_validacion_id'])) % 9000 + 1000}",
        "mensaje": "Documento entregado al sistema académico SIMULADO (contrato respetado).",
    }
