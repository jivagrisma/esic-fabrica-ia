# Entregable 2 — Plan de Implementación

**Fábrica de IA y Automatización ESIC Medellín** · Versión 1.0 (borrador) · 2026-09-16
Autor: Jorge Iván Aguirre · Asistido por Claude Code

> Punto de partida real: el **micro-MVP ya está desplegado y demostrable** en Cloud Run (chatbot con Vertex AI Gemini + validador con Document AI + Firestore). Este plan describe el camino desde esa base demostrada hasta producción con integraciones reales y gobierno de datos.

---

## 1. Fases del proyecto

### Fase 0 — Análisis y datos (2 semanas)

**Objetivo:** convertir los datos demo en bases de conocimiento y reglas reales de ESIC.

- Inventario de consultas frecuentes (admisiones, financicería/financiamiento, empleo/egresados) y clasificación por volumen.
- Curation de la KB institucional: programas vigentes, fechas, requisitos, políticas de financiamiento, bolsa de empleo. Fuente única versionada.
- Definición de tipologías documentales a validar (cédula, transcripts, certificados) y reglas de validación por tipo (campos exigidos, formatos, umbrales de confianza).
- Muestreo de documentos reales (anonimizados) para calibrar OCR y umbrales.
- Levantamiento técnico de integraciones: acceso a CRM (p. ej. Dynamics/HubSpot), SIA, Microsoft 365 (Graph API), permisos y firewalls.
- Matriz de datos personales (Habeas Data, Ley 1581 de 2012): qué dato, para qué, dónde se almacena, cuánto se retiene.

**Hitos verificables:** KB v1 aprobada por el negocio; catálogo de reglas de validación firmado; inventario de acceso a integraciones confirmado con TI ESIC.

### Fase 1 — MVP endurecido (4 semanas)

**Objetivo:** llevar el micro-MVP ya demostrado a calidad piloto con datos reales y usuarios piloto.

- Migrar la KB demo por la KB real curada (mismo contrato, contenido real).
- Chatbot: afinado de prompts, reglas de derivación a humano con contexto, manejo de fuera-de-dominio; logging completo en `interactions`.
- Validador: reglas deterministas + análisis semántico Gemini calibradas con el muestreo de Fase 0; veredictos ✅/⚠️/❌ con trazabilidad.
- Seguridad piloto: Identity Platform o IAP para acceso autenticado; service accounts de mínimo privilegio; sin PII en logs.
- Pruebas E2E automatizadas (Playwright) y set de regresión de respuestas del chatbot.
- Piloto controlado con un equipo pequeño (p. ej. 2-3 personas de admisiones) y dataset de documentos etiquetado.

**Hitos verificables:** piloto interno en uso diario; ≥90% de respuestas del chatbot evaluadas como correctas en set de prueba; reporte de validación de 20+ documentos reales comparado contra revisión manual.

### Fase 2 — Integraciones reales (4 semanas)

**Objetivo:** sustituir los conectores simulados por integraciones productivas (los contratos JSON Schema ya existen).

- CRM real: creación/actualización de casos desde el chatbot (tickets con transcripción), sincronización de estados.
- SIA: entrega real de solicitudes validadas (reemplaza el conector simulado de "entrega"); manejo de errores y reintentos.
- Microsoft Graph: notificaciones y gestión documental en Microsoft 365 (correo/equipos según el flujo de admisiones).
- Identidad: SSO institucional para usuarios internos y, si aplica, para estudiantes.
- Migración de datos del piloto; plan de reversión (roll-back a proceso manual) documentado.

**Hitos verificables:** end-to-end real: consulta → ticket en CRM → resolución; documento → validación → registro en SIA sin digitación manual; integraciones cubiertas por tests de contrato.

### Fase 3 — Escalamiento y gobierno (4 semanas)

**Objetivo:** abrir a toda la población objetivo y operar con métricas y cumplimiento.

- Vertex AI Search / RAG productivo sobre la KB (grounding auditable, citas a fuente).
- Escenario 3 (recomendador de programas) en producción sobre datos de empleabilidad, con explicabilidad y auditoría de sesgos por cohorte.
- Dashboard de métricas: % resolución sin humano, % auto-validación, latencia, CSAT, costo por interacción.
- DLP API: enmascaramiento de PII antes de almacenamiento analítico; retención y borrado conforme a Ley 1581.
- Gobierno: políticas de datos, gestión de prompts/modelos como activos versionados, presupuesto y alertas de costo GCP, capacitación y plan de adopción.
- Aumento de cuotas de Document AI según demanda proyectada.

**Hitos verificables:** lanzamiento general; dashboard operativo con baseline de métricas; política de tratamiento de datos aprobada por jurídico; escenario 3 en producción.

---

## 2. Timeline (14 semanas)

| Semanas | Fase | Hitos verificables de cierre |
|---|---|---|
| 1–2 | Fase 0 — Análisis y datos | KB v1 aprobada · reglas de validación firmadas · accesos de integración confirmados · matriz Habeas Data |
| 3–6 | Fase 1 — MVP endurecido | Piloto interno activo · ≥90% respuestas correctas en set de prueba · 20+ documentos reales validados vs revisión manual |
| 7–10 | Fase 2 — Integraciones reales | CRM + SIA + Microsoft Graph productivos · flujo end-to-end sin digitación manual · tests de contrato en CI |
| 11–14 | Fase 3 — Escalamiento y gobierno | Lanzamiento general · RAG productivo · recomendador en producción · dashboard de métricas · DLP + política Ley 1581 |

Supuesto de calendario: equipo dedicado según la sección 3 y disponibilidad de TI ESIC para las integraciones de Fase 2. Un retraso en accesos/permisos de integración desplaza Fase 2 semana a semana.

---

## 3. Recursos

### 3.1 Equipo

| Rol | Dedicación | Responsabilidad principal |
|---|---|---|
| PM / líder de producto | 1 FTE | Alcance, coordinación con ESIC, adopción, reporte al comité |
| Ingeniero IA / Fullstack | 1–2 FTE | Vertex AI, Document AI, Cloud Run, conectores, tests |
| Analista de datos | 1 FTE (Fases 0–1, parcial luego) | KB, reglas de validación, etiquetado, métricas/dashboard |
| QA | ~0.5 FTE (parcial) | Sets de prueba, regresión de chatbot, verificación documental |
| TI ESIC (soporte) | Parcial, crítico en Fase 2 | Accesos a CRM, SIA, Microsoft 365, red y permisos |

Total aproximado: 3–4 FTE equivalentes en las semanas pico.

### 3.2 Infraestructura

Todo GCP gestionado (serverless), ya provisionado en el proyecto `esic-fabrica-ia`: Cloud Run, Vertex AI (Gemini), Document AI, Firestore, Cloud Build/Artifact Registry. Sin servidores que administrar; escala de 0 a N automáticamente.

### 3.3 Costos de nube estimados (MVP / piloto)

| Servicio | Estimación mensual | Supuesto |
|---|---|---|
| Cloud Run | USD 10–30 | Tráfico demo/piloto, escala a cero, pago por uso |
| Vertex AI — Gemini (flash) | USD 50–200 | Modelos flash, según volumen de consultas y análisis documental |
| Document AI | ~USD 1.50 por 1.000 páginas | Precio de lista del processor OCR; crece linealmente con volumen |
| Firestore | Capa gratuita → USD 20–100 | Lecturas/escrituras del piloto; crecimiento con adopción |
| **Total MVP/piloto** | **~USD 80–350/mes** | Escala con volumen real de producción |

> **Declaración:** estas cifras son **estimaciones de precio de lista** de Google Cloud (sin descuentos ni negociación) y no constituyen una cotización. El costo productivo depende del volumen final de consultas y documentos; el dashboard de Fase 3 incluye costo por interacción para gobernarlo.

---

## 4. Riesgos y mitigación

| # | Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|---|
| 1 | Calidad del OCR en documentos escaneados de baja calidad (fotocopias, fotos de celular) | Alto: falsos ⚠️/❌, retrabajo | Media-alta | Umbral de confianza por campo; veredicto ⚠️ con alerta específica en vez de rechazo; calibración con muestreo real en Fase 0; pedir re-carga guiada al usuario |
| 2 | Alucinaciones del LLM (respuestas inventadas sobre programas/fechas/financiamiento) | Alto: confianza y reputación | Media | Grounding estricto en KB curada versionada; reglas de fuera-de-dominio; derivación a humano; set de regresión de respuestas en CI; RAG con citas en Fase 3 |
| 3 | Resistencia al cambio del equipo administrativo | Alto: baja adopción, sombra de proceso manual | Media | Involucrar al equipo desde Fase 0; piloto con dueños del proceso; capacitación; mostrar ahorro de tiempo con sus propias métricas; derivación a humano como red de seguridad, no como amenaza |
| 4 | Datos personales / Habeas Data (Ley 1581 de 2012, Colombia) | Alto: legal y reputacional | Media | Matriz de tratamiento en Fase 0; anonimización del muestreo; DLP + retención limitada + CMEK en Fase 3; aprobación de jurídico antes de datos reales |
| 5 | Dependencia de un solo proveedor cloud (Google) | Medio: costo/continuidad a largo plazo | Media | Arquitectura en contenedores estándar (Cloud Run) y contratos de integración portables; LLM detrás de una variable de configuración; evaluar multicosto/multi-modelo solo si hay señales de precio o discontinuidad |
| 6 | Cuotas de Document AI (limitación de throughput) | Medio: cuello de botella en picos de admisión | Media | Solicitar aumento de cuota anticipado; cola con reintentos; procesamiento por lotes fuera de horas pico; monitoreo de cuota en el dashboard |
| 7 | Baja adopción del chatbot por usuarios (prefieren el canal humano) | Medio: no se materializa el ahorro | Media | Canal único visible (web/WhatsApp según hábitos del estudiante); respuestas rápidas y útiles desde el día 1; medir y publicar % de resolución; derivación sin fricción con contexto |
| 8 | Retraso en accesos a integraciones (CRM/SIA/Microsoft) por permisos internos | Medio: desplaza Fase 2 | Alta | Gestionar accesos desde Fase 0 con TI ESIC; conectores simulados permiten avanzar en paralelo; contratos JSON Schema ya definidos |

---

## 5. Criterios de salida por fase (Definition of Done)

**Fase 0**
- [ ] KB institucional v1 revisada y aprobada por el dueño de negocio.
- [ ] Catálogo de reglas de validación por tipo documental firmado.
- [ ] Accesos técnicos a CRM, SIA y Microsoft Graph confirmados (o plan con fecha).
- [ ] Matriz de tratamiento de datos personales (Ley 1581) revisada por jurídico.

**Fase 1**
- [ ] Piloto interno en uso diario por el equipo de admisiones durante ≥2 semanas.
- [ ] ≥90% de respuestas correctas en set de regresión de chatbot (≥100 casos).
- [ ] ≥20 documentos reales validados con concordancia ≥95% contra revisión manual.
- [ ] Autenticación activa; sin PII en logs; tests E2E automatizados en CI.

**Fase 2**
- [ ] Flujo end-to-end real: consulta → ticket CRM → resolución; documento → validación → SIA, sin digitación manual.
- [ ] Tests de contrato para los tres conectores en pipeline CI.
- [ ] Plan de reversión documentado y probado una vez.

**Fase 3**
- [ ] Lanzamiento general a estudiantes/egresados/empresas aliadas.
- [ ] Vertex AI Search/RAG productivo con respuestas citando fuente.
- [ ] Escenario 3 (recomendador) en producción con auditoría de sesgos.
- [ ] Dashboard operativo con baseline de métricas y presupuesto con alertas.
- [ ] DLP activo y política de retención/borrado conforme a Ley 1581.

---

*Documento borrador para revisión del comité técnico de ESIC. Estimaciones de costo: precio de lista, no cotización.*
