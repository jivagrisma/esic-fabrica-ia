# Entregable 5 — Presentación Ejecutiva (1 página)

**Fábrica de IA y Automatización ESIC Medellín** · 2026-09-16 · Jorge Iván Grisales Marin

---

## El problema, en números

| Dato | Valor | Fuente |
|---|---|---|
| Tiempo del equipo en tareas repetitivas | **~60%** | Enunciado del caso |
| Validación documental manual | **2 h por 20 solicitudes** (6 min c/u) | Enunciado del caso |
| Respuesta actual a consultas de estudiantes | Horas a días, en horario laboral | Enunciado del caso |

## La solución — DESPLEGADA Y VERIFICADA EN VIVO

**👉 Pruébala ahora: https://esic-fabrica-ia-985215895070.us-central1.run.app**

> Entorno **vivo en refinamiento continuo** (no una demo congelada): se siguen iterando el código
> y la calidad de respuesta tras esta entrega; el servicio permanece disponible.

Plataforma 100% **Google Cloud gestionado (serverless)** — sin servidores que administrar, escala de 0 a N sola:

1. **Chatbot inteligente** — IA generativa (Vertex AI Gemini) con base de conocimiento institucional: responde en segundos 24/7 y deriva a humano **con contexto y ticket** cuando toca. *Verificado en vivo.*
2. **Validación automática de documentos** — OCR (Document AI) + reglas + IA que extrae, valida y entrega al sistema académico; el equipo humano solo revisa las alertas ⚠️. *Verificado en vivo: extracción de campos con 98% de confianza y detección de inconsistencias por IA.*
3. **Recomendador de programas** (nivel diseño) — recomendación explicable con datos de empleabilidad.

**Estado real al cierre:** escenarios 1 y 2 desplegados en Cloud Run (revision esic-fabrica-ia-00003-rnb) y probados end-to-end vía HTTP: chat con respuesta grounded, interacciones persistidas en Firestore (IDs reales), validación de cédula con reporte VAL-* y entrega al SIA simulado con recibo REC-*. Las integraciones con CRM, SIA y Microsoft 365 son **conectores simulados con contratos documentados** — así se declara, sin excepciones. El ID de modelo Gemini no se verificó contra la API en vivo (documentado en el Entregable 1) pero las llamadas reales funcionan contra el servicio desplegado.

## Por qué es la mejor opción

| Criterio | Esta solución | Alternativa típica |
|---|---|---|
| Tiempo a primer demo | Días (serverless, un solo servicio) | Meses (plataforma on-premise o multi-servicio) |
| Carga operativa para escalar | Casi cero (gestionado, autoscaling) | Equipo de operación dedicado |
| Costo MVP/piloto | **~USD 80–350/mes** (precio de lista, no cotización) | Miles en licencias/infra fija |
| Riesgo de datos | PII en tenant propio, DLP y Ley 1581 en el roadmap | PII en APIs externas sin control |
| Honestidad de alcance | Simulado vs. real declarado en cada conector | "Integrado" sin evidencia |

## El retorno (modelo con supuestos declarados)

| Concepto | Valor | Supuesto |
|---|---|---|
| Horas liberadas por mes | **~625 h** (~3.5 FTE) | 300 consultas/día, 70% auto-resueltas, 8 min/consulta; 1 lote de 20 solicitudes/día de 2 h → 15 min |
| Ahorro anual valorizado | **~USD 52.500** | Hora a USD 7 (cargo ~USD 1.200/mes, Colombia) |
| Costo año 1 | **~USD 47.900** | Infra ~USD 3.600 + 1.5 FTE ~USD 42.000 + contingencia |
| **Payback** | **~11–16 meses** | Escenarios optimista/base (ver Entregable 4) |

## Siguientes pasos (decisión que se pide hoy)

1. **Aprobar Fase 0 (2 semanas):** validar el supuesto crítico — volumen real de consultas/día — y curar la KB institucional real.
2. **Piloto interno (4 semanas):** equipo de admisiones usando la solución con datos reales anonimizados.
3. **Integraciones reales (4 semanas):** sustituir conectores simulados por CRM, SIA y Microsoft Graph (contratos ya definidos).
4. **Escalamiento y gobierno (4 semanas):** RAG productivo, recomendador, dashboard de métricas, DLP y cumplimiento Ley 1581.

**Total: 14 semanas de piloto a producción**, con puntos de decisión verificables al cierre de cada fase.

---

*Detalles: Entregables 1–4 en `entregables_finales/`. Cifras de ROI: modelo de estimación con supuestos declarados, no auditoría. Costos: precio de lista GCP, no cotización.*
