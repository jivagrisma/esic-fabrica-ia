# Entregable 1 — Arquitectura de la Solución

**Fábrica de IA y Automatización ESIC Medellín** · Versión 1.0 · 2026-09-16
Autor: Jorge Iván Grisales Marín

---

## 1. Resumen ejecutivo

Plataforma de IA sobre **Google Cloud 100% gestionado (serverless)** que ataca el 60% de tiempo
perdido en consultas repetitivas y procesos manuales con tres capacidades:

1. **Chatbot inteligente** (Escenario 1) — IA generativa con grounding en base de conocimiento institucional, derivación a humano con contexto y registro de cada interacción.
2. **Validación automática de documentos** (Escenario 2) — OCR + IA que extrae, valida, alerta y entrega al sistema académico.
3. **Recomendador de programas** (Escenario 3, nivel diseño) — recomendación explicable con datos de empleabilidad.

Principio rector: **no reconstruir lo que la nube ya resuelve gestionado** — Vertex AI, Document AI,
Firestore y Cloud Run dan minutos de despliegue y escala sin carga operativa adicional, que es
exactamente el requisito del caso ("escalar sin incrementar significativamente la carga operativa").

**Estado real al cierre de la sesión:** los escenarios 1 y 2 están implementados en el repo; el despliegue a Cloud Run y la verificación E2E se ejecutan al cierre de esta sesión.

## 2. Componentes principales

```
                    ┌────────────────────────────────────────────────────────┐
                    │                      GOOGLE CLOUD                      │
 Estudiantes /      │  ┌──────────────────────────────────────────────────┐  │
 Egresados /    ────┼─►│  Cloud Run (FastAPI)                             │  │
 Empresas /         │  │  · UI web (chat + validador)                     │  │
 Comité evaluador   │  │  · /api/chat      → Escenario 1                 │  │
 (link público)     │  │  · /api/documents → Escenario 2                 │  │
                    │  └───────┬───────────────┬───────────────┬──────────┘  │
                    │          │               │               │             │
                    │          ▼               ▼               ▼             │
                    │  ┌──────────────┐ ┌─────────────┐ ┌──────────────┐    │
                    │  │ Vertex AI    │ │ Document AI │ │ Firestore    │    │
                    │  │ Gemini       │ │ OCR/Parser  │ │ (Native)     │    │
                    │  │ (LLM)       │ │ + Form      │ │ interactions │    │
                    │  └──────┬───────┘ └──────┬──────┘ │ tickets      │    │
                    │         │                │        │ validations  │    │
                    │         ▼                ▼        └──────────────┘    │
                    │  ┌──────────────────────────────┐                     │
                    │  │ Conectores SIMULADOS (docs)  │                     │
                    │  │ CRM · SIA académico · MS 365 │                     │
                    │  └──────────────────────────────┘                     │
                    └────────────────────────────────────────────────────────┘
```

| Componente | Servicio GCP | Rol | Por qué este servicio |
|---|---|---|---|
| Orquestación + API + UI | **Cloud Run** | Un solo servicio sirve la web y la API; autoscaling de 0 a N | Serverless, contenedor estándar, link público en minutos, paga por uso |
| LLM chatbot + análisis | **Vertex AI — Gemini** (`gemini-2.5-flash`)* | Respuestas generativas con grounding; análisis de consistencia de documentos; explicaciones del recomendador | Modelo GA estable, bajo costo/latencia, RAG nativo (Vertex Search) para producción, data governance empresarial |
| OCR + extracción | **Document AI** (región multi-región **`us`**) | Digitaliza cédula/transcripts/certificados, extrae pares clave-valor y confianza por campo | OCR de precisión líder + parsers por tipo de documento + confidence scores listos para reglas de validación |
| Estado + registro | **Firestore (Native)** | Colecciones `interactions`, `tickets`, `validations` | Serverless, latencia baja, escala automática, integración nativa con Cloud Run |
| Integraciones | **Conectores simulados** (`connectors/`) | Contratos (JSON Schema) + respuestas simuladas de CRM, sistema académico y Microsoft 365 | El caso NO exige integración productiva; se documenta como simulada (requisito de honestidad del reto) |

\* **Nota de verificación (honestidad del ejercicio):** el ID de modelo `gemini-2.5-flash`
**no se verificó contra la API en vivo** durante la construcción — el intento de listar los
publisher models de Vertex AI falló repetidamente por límites de tiempo y configuración de
quota project, y se decidió no gastar más tiempo del bloque en depurarlo. Es el ID GA estable
según el conocimiento del autor al corte de esta solución y **debe confirmarse en el panel de
Vertex AI Model Garden (o con la lista de publisher models) al momento del despliegue real**.
La arquitectura no depende del ID específico: cambiar de modelo = ajustar 1 variable de
entorno (`GEMINI_MODEL` en `app/config.py`).

**Decisión de regiones (explícita, no inconsistencia):** este proyecto despliega Cloud Run y
Vertex AI en `us-central1`, pero Document AI opera en su **región multi-región `us`**
(`documentai.googleapis.com/.../locations/us/...`) — así lo exige la API para este proyecto
(una request a `locations/us-central1` es rechazada con "must match the server deployment 'us'").
El processor OCR creado para el MVP es
`projects/985215895070/locations/us/processors/33966db067a8aeba` (estado: ENABLED).
Esta división no afecta latencia ni costo de forma significativa y queda documentada como
decisión deliberada de la implementación.

## 3. Flujo de datos

### 3.1 Escenario 1 — Chatbot (E1 → E3)

```
Usuario → POST /api/chat {mensaje, session_id}
  1. Cloud Run recibe; carga la KB institucional (programas, financiamiento, empleo —
     base curada versionada en el repo, datos sintéticos en el MVP).
  2. Prompt armado con: system prompt (dominio ESIC + reglas de derivación y de fuera-de-dominio)
     + KB (grounding) + mensaje. Salida forzada a JSON (response_mime_type).
  3. Gemini responde SOBRE la KB (reduce alucinación); si detecta intención de derivación
     (queja, caso financiero complejo, sin respuesta en KB) → crea ticket vía conector CRM
     simulado con transcripción completa.
  4. La interacción completa se persiste en `interactions` (análisis posterior).
  5. Respuesta al usuario; si hubo derivación, incluye #ticket y contacto directo.
```

### 3.2 Escenario 2 — Validación de documentos (E2 → E3)

```
Admisiones → POST /api/documents (multipart: PDF/imagen + tipo de documento + ID solicitud)
  1. Cloud Run guarda el binario y llama Document AI (OCR processor) → texto completo +
     confianza media por páginas.
  2. Motor de reglas (determinístico): completitud (¿están los campos exigidos para el tipo?),
     integridad (confidence < umbral, documento ilegible), formato (cédula 6-10 dígitos),
     consistencia (nombre del solicitante vs documento).
  3. Gemini (análisis semántico): inconsistencias que las reglas no ven — p. ej. nombre del
     transcript ≠ nombre de la cédula, fechas imposibles, señales de alteración en el texto.
  4. Veredicto: ✅ válido · ⚠️ alerta (con hallazgos) · ❌ rechazado. Reporte JSON persistido
     en `validations`.
  5. Si ✅/⚠️ → conector SIMULADO al sistema académico (contrato REST documentado; en el MVP
     devuelve la respuesta esperada con el payload que se enviaría). Notificación Teams simulada
     solo si hay hallazgos.
```

Detalle completo del código, prompts y defensas por capa: Entregable 3.

### 3.3 Escenario 3 — Recomendador (diseño; implementación fuera de alcance por tiempo)

Perfil del estudiante (habilidades, intereses, carrera previa) + catálogo de programas +
datos de empleabilidad de egresados → RAG (Vertex Search) + Gemini con prompt que exige
**recomendación explicable** (3 opciones, justificación por opción, data de empleabilidad citada).
Sesgos: el ranking se restringe a factores ocupacionales, se excluyen atributos protegidos y
se auditan recomendaciones por cohorte (detalle en Entregable 3).

## 4. Tecnologías seleccionadas y justificación

| Decisión | Alternativas | Por qué GCP gestionado |
|---|---|---|
| Vertex AI vs API externa (OpenAI/etc.) | APIs de terceros | Datos institucionales permanecen en el tenant de Google; control de acceso por IAM; sin egress de PII a terceros; misma experiencia operativa que el resto del stack |
| Document AI vs Tesseract/self-hosted | OCR propio | Mantenimiento cero, precisión superior en documentos latinos, confidence por campo (base de las reglas de validación) |
| Cloud Run vs GKE/VMs | K8s, Compute Engine | Escala de 0 a N sin operación; costo por uso (demo casi gratis); despliegue con 1 comando |
| Firestore vs SQL gestionado | Cloud SQL | El registro es documental y de acceso por clave; elimina administrar BD en un MVP |
| FastAPI + UI estática vs framework full-stack | Next.js/Django | Sin build de frontend = menos piezas, despliegue más rápido — el criterio del reto es el link vivo, no la UI |

## 5. Seguridad

**MVP (lo desplegado — declarado explícitamente):**
- Servicio Cloud Run con invocación pública (necesario para que el comité lo pruebe sin fricción).
- Datos demo sintéticos: sin PII real de estudiantes.
- Credenciales: la app se autentica por ADC/service account del runtime — **cero claves en el código o el repo** (auditoría de secretos hecha pre-apertura del repo público).
- Prompt-injection: el contenido de los documentos se pasa a Gemini como dato (delimitado entre etiquetas `<documento>`), no como instrucción; inyección probada como caso de test.

**Diseño productivo (documentado, no implementado en el MVP):**
- Identidad: Identity Platform (estudiantes/egresados) + IAP o Sign-in with Google para el panel interno.
- IAM de mínimo privilegio: SA de Cloud Run solo con `roles/aiplatform.user`, `roles/documentai.user`, `roles/datastore.user`.
- Datos: CMEK, retención limitada, DLP API para enmascarar PII antes de enviar a almacenamiento de análisis.
- Cumplimiento: Habeas Data (Ley 1581 COL) para tratamiento de datos personales; documento "simulado vs real" como política de gobierno.
- Auditoría: Cloud Audit Logs + alertas de presupuesto.

## 6. Escalabilidad y operación

- **Horizontal automática:** Cloud Run escala por concurrencia (0 → N instancias); sin intervención humana = "escalar sin cargar la operación", requisito del caso.
- **Cuellos reales documentados:** cuota de Document AI (se solicita increase vía Google Cloud console) y costo de tokens de Gemini (se mitiga con modelos flash + caché de contexto).
- **Degradación elegante:** si Firestore falla, la interacción del usuario no falla (registro best-effort).
- **Observabilidad:** Cloud Logging estructurado por request; métricas: latencia p95, tasa de derivación a humano, % documentos auto-validados, costo/1k interacciones.
- **Evolución:** el MVP vive en un proyecto aislado (`esic-fabrica-ia`); pasar a producción = habilitar identidad + apuntar conectores simulados a los sistemas reales (los contratos ya están definidos en `connectors/`).

## 7. Declaración de integridad

Los integradores con CRM, sistema académico y Microsoft 365 son **simulados y están documentados
como tales**. Ningún sistema real de ESIC fue accedido ni afectado. Los datos institucionales
(programas, financiamiento, empleo) son sintéticos de demostración. El modelo `gemini-2.5-flash`
no se verificó en vivo (ver §2) y el despliegue a Cloud Run se ejecuta al cierre de esta sesión.

---
*Diagramas en texto para portabilidad; versión Mermaid disponible en el repo si se requiere render.*
