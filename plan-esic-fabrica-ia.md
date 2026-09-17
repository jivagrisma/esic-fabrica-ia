# Plan de Ejecución — Fábrica de IA ESIC (sesión 2026-09-16)

> Registro vivo de la sesión. Presupuesto total: 2h30. Cada tarea se marca `[x]` al cerrarse.

## Infraestructura base (pre-bloque 1) — DONE

- Repo GitHub privado: `github.com/jivagrisma/esic-fabrica-ia` ✅
- Proyecto GCP: `esic-fabrica-ia` (nº 985215895070) ✅
- Billing: vinculado a cuenta `014D68-XXXXXX-XXXXXX` (ID redactado: no exponer en repo público) ✅
  - Nota: se desvinculó `project-a88bf383-099d-4d78-960` (verificado vacío: sin APIs de cómputo) por cuota de la cuenta. Autorizado por Jorge.
- APIs habilitadas: Cloud Run, Vertex AI, Document AI, Firestore, Cloud Build, Artifact Registry ✅
- Región de trabajo: `us-central1` (Cloud Run, Vertex AI, Firestore) · Document AI usa multi-región `us`
- Processor Document AI OCR: `projects/985215895070/locations/us/processors/33966db067a8aeba` (ENABLED) ✅
- Firestore (default) creado en us-central1 ✅

---

## FASE 1 — Requirements (qué y para quién)

### Dolor raíz
Equipos de admisiones/estudiantes/administrativo dedican ~60% del tiempo a consultas
repetitivas y procesos manuales (validación de documentos: ~2h por 20 solicitudes).
Si no se hace: el cuello de botella escala con la demanda y las decisiones estratégicas se retrasan.

### Escenarios elegidos para desarrollo técnico profundo: 1 y 2 (por defecto del caso)

| # | Escenario | Actor principal | Qué resuelve | Qué pasa si no se hace |
|---|-----------|-----------------|--------------|------------------------|
| 1 | Chatbot inteligente de consultas | Estudiante, egresado, empresa aliada | Respuesta inmediata 24/7 sobre programas, financiamiento y empleo con IA generativa; derivación a humano con contexto; registro de interacciones | Consultas siguen cayendo al equipo humano; respuesta en horas/días |
| 2 | Validación automática de documentos | Admisiones | OCR + IA que extrae datos, valida integridad/completitud, alerta inconsistencias y "entrega" al sistema académico | 2h/20 solicitudes de trabajo manual; errores humanos; demora en admisiones |
| 3 | Recomendador de programas (solo diseño + prompts) | Estudiante nuevo | Recomendación explicable de especializaciones con datos de empleabilidad | Asesoramiento manual lento; queda en nivel de diseño por límite de tiempo |

### Alcance del micro-MVP (link vivo)
Un solo servicio en Cloud Run con:
- `/` — UI web simple (HTML/JS sin build step) con dos módulos: Chat ESIC y Validador de documentos.
- `/api/chat` — Escenario 1: LLM en Vertex AI + base de conocimiento curada (programas/financiamiento/empleo), derivación a humano con contexto, logging en Firestore.
- `/api/documents` — Escenario 2: upload de documento → Document AI (OCR/extracción) → validaciones de reglas + LLM → reporte con alertas → conector **simulado** al sistema académico.
- Firestore: colecciones `interactions`, `tickets`, `validations` (registro y análisis posterior).

### Integraciones (explícito: SIMULADAS)
- CRM (p. ej. Dynamics/HubSpot), base de datos académica (SIA) y sistemas Microsoft (365/Graph):
  se implementan como módulos `connectors/` con contratos (JSON schema) documentados y respuestas
  simuladas. En documentos se declaran como **conectores simulados, no integraciones productivas**.

## FASE 2 — Design (arquitectura del micro-MVP)

```
Usuario (comité / demo)
   │ HTTPS
   ▼
Cloud Run (FastAPI, 1 servicio, autoscaling)  ── sirve UI + API
   ├── Vertex AI (Gemini) ── chatbot con grounding en KB curada + análisis de documentos
   ├── Document AI (OCR/Parser) ── extracción de texto y campos de cédula/transcript/certificado
   ├── Firestore (Native) ── interactions / tickets / validations
   └── connectors/ (SIMULADOS) ── CRM, sistema académico, Microsoft 365
```

- Lenguaje: Python 3.12 + FastAPI. UI: HTML/JS estático. Sin build frontend → minutos de despliegue.
- LLM: Gemini vía Vertex AI (`gemini-2.5-flash`; ID a verificar en bloque 3 con lista real de modelos).
- Document AI: processor OCR (se crea por CLI en bloque 3).
- Seguridad MVP: servicio público sin datos personales reales (documentado); diseño productivo con
  Identity Platform/IAP,least privilege por SA, CMEK y retención — se describe en Entregable 1.
- Escalabilidad: Cloud Run autoscaling serverless; los cuellos serían quotas de Document AI (documentado).

## FASE 3 — Tasks (atómicas, por entregable)

| ID | Tarea | Entregable | Bloque |
|----|-------|-----------|--------|
| T1 | Documento arquitectura completo | E1 | 2 | [x] docs/01 + entregables_finales/01 |
| T2 | Scaffolding repo (FastAPI + UI base + Dockerfile) | — | 3 | [x] |
| T3 | KB curada ESIC (programas/financiamiento/empleo, datos demo) | — | 3 | [x] app/kb.py |
| T4 | Escenario 1: endpoint chat + grounding + derivación + logging | E3 | 3 | [x] app/scenario1_chat.py — verificado en vivo |
| T5 | Escenario 2: upload + Document AI + validaciones + alertas + conector simulado | E3 | 3 | [x] app/scenario2_docs.py — verificado en vivo (VAL-8F34AD74, conf 98%) |
| T6 | Escenario 3: prompt/pseudocódigo (nivel diseño) | E3 | 3 | [x] sección en entregables_finales/03 |
| T7 | Deploy Cloud Run + link público | — | 4 | [x] https://esic-fabrica-ia-985215895070.us-central1.run.app (rev 00003-rnb) |
| T8 | Verificación E2E con Playwright (chat + documento) | — | 4 | [x] vía curl HTTP (health/UI/chat/docs). Playwright: omitido por límite de tiempo, flujo probado por API |
| T9 | Plan de Implementación (fases/timeline/recursos/riesgos) | E2 | 5 | [x] entregables_finales/02 |
| T10 | Evaluación de Impacto y ROI | E4 | 5 | [x] entregables_finales/04 |
| T11 | Presentación Ejecutiva 1 página | E5 | 5 | [x] entregables_finales/05 (con URL real) |
| T12 | Checkpoint + ZIP final + cierre de este plan | — | 6 | [x] |

## Cierre de sesión — resultado real

- **Link vivo verificado**: https://esic-fabrica-ia-985215895070.us-central1.run.app
  - `/health` OK · UI OK · `/api/chat` OK (respuesta grounded, Firestore con interaction_id real) ·
    `/api/documents` OK (OCR 98% conf, alertas semánticas IA, entrega SIA simulada con recibo).
- Fixes reales durante la sesión: Dockerfile sin copiar `connectors/`; Page.confidence → page.layout.confidence (SDK Document AI); rol correcto roles/documentai.apiUser.
- Pendiente honesto: verificación visual con Playwright, testing adversarial del chatbot, escenario 3 en producción.

Paralelización (Agent Teams desde bloque 3): T4 (chatbot) ∥ T5 (documentos) ∥ T9/T10 (borradores narrativos con diseño del bloque 2).

## Decisiones tomadas en sesión

- 2026-09-16: **Repo GitHub es PUBLICO desde este punto** (`https://github.com/jivagrisma/esic-fabrica-ia`).
  Auditoría de secretos hecha ANTES de cambiar visibilidad (historial completo + árbol limpio:
  sin API keys, credenciales, SA JSON, .env ni IDs de billing; ID de billing redactado de este plan).
  En Bloque 6 NO repetir la auditoría desde cero: solo revisar lo agregado después de este punto.
  Regla: nunca commitear claves/credenciales; el despliegue usará ADC/SA de gcloud, no archivos JSON en el repo.

- 2026-09-16: billing resuelto desvinculando proyecto vacío (autorizado por Jorge).
- 2026-09-16: escenario 3 queda en diseño/prompt por restricción de tiempo (regla del caso: 2 profundos).
