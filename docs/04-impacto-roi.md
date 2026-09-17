# Entregable 4 — Evaluación de Impacto y ROI

**Fábrica de IA y Automatización ESIC Medellín** · Versión 1.0 (borrador) · 2026-09-16
Autor: Jorge Iván Aguirre · Asistido por Claude Code

> **Advertencia de método:** lo que sigue es un **modelo de estimación con supuestos declarados**, no una auditoría financiera. Cada cifra lleva su supuesto al lado. El comité puede cambiar cualquier supuesto y recalcular; la aritmética se muestra paso a paso.

---

## 0. Base cuantitativa del caso (supuestos del enunciado + estimaciones)

| Supuesto | Valor | Fuente |
|---|---|---|
| Tiempo del equipo en tareas repetitivas | ~60% | Enunciado del caso |
| Validación documental actual | 2 horas por 20 solicitudes (6 min/solicitud) | Enunciado del caso |
| Objetivo de reducción de trabajo manual | 70% | Enunciado del caso |
| Consultas atendibles por chatbot | 300/día hábil | Estimación (a calibrar en Fase 0) |
| Días hábiles por mes | 21 | Estimación estándar |
| Valorización de hora liberada | USD 7/hora | Estimación: cargo administrativo/técnico Colombia ~USD 1,200/mes ÷ ~176 h/mes ≈ USD 6.8/h (redondeado) |

---

## 1. Ahorro operativo

### 1.1 Chatbot (Escenario 1)

| Paso | Cálculo | Resultado |
|---|---|---|
| Consultas por día hábil | supuesto | 300 |
| % resueltas sin humano | objetivo | 70% |
| Consultas desviadas del equipo humano/día | 300 × 0.70 | 210 |
| Tiempo ahorrado por consulta desviada | supuesto | 8 min |
| Minutos ahorrados por día | 210 × 8 | 1.680 min |
| Horas ahorradas por día | 1.680 ÷ 60 | **28 h/día** |
| Horas ahorradas por mes | 28 × 21 días hábiles | **588 h/mes** |
| Valorización mensual | 588 h × USD 7/h | **USD 4.116/mes** |

Nota: las 8 min representan el tiempo promedio que hoy consume atender una consulta repetitiva (respuesta + contexto + seguimiento). A calibrar con mediciones de Fase 0.

### 1.2 Validación documental (Escenario 2)

| Paso | Cálculo | Resultado |
|---|---|---|
| Lote de referencia | enunciado | 20 solicitudes |
| Tiempo actual por lote | enunciado | 120 min (2 h) |
| Tiempo con revisión asistida (solo ⚠️ alertas) | estimación | 15 min |
| Ahorro por lote | 120 − 15 | **105 min (1.75 h)/lote** |
| Reducción de esfuerzo | 105 ÷ 120 | **87.5% del ciclo** |
| Ciclos por mes | supuesto: 1 lote/día hábil | 21 lotes |
| Horas ahorradas por mes | 1.75 × 21 | **36.75 h/mes** |
| Valorización mensual | 36.75 h × USD 7/h | **USD 257/mes** |

Nota: el objetivo declarado del caso es reducir 70% el trabajo manual; el escenario de validación lo supera (87.5%) porque la revisión asistida solo interviene sobre alertas. Si se usa la meta conservadora de 70%, el ahorro por lote sería 84 min (1.4 h → 29.4 h/mes). El cálculo principal usa el escenario asistido.

### 1.3 Ahorro total operativo

| Concepto | Horas/mes | USD/mes (a USD 7/h) |
|---|---|---|
| Chatbot | 588 | 4.116 |
| Validación documental | 36.75 | 257 |
| **Total** | **~625 h/mes** | **~USD 4.373/mes** |
| **Run-rate anual** | **~7.500 h/año** | **~USD 52.500/año** |

Contexto: 625 h/mes equivale a ~3.5 FTE de capacidad recuperada (a 176 h/mes), contra ~60% del tiempo hoy en tareas repetitivas — coherente con el objetivo del caso.

---

## 2. Beneficios por usuario

| Usuario | Beneficio | Magnitud |
|---|---|---|
| Estudiante / egresado | Respuesta en segundos, 24/7, vs horas-días por canal humano | De horas-días a < 30 seg |
| Empresa aliada | Canal inmediato para vacantes, convenios y consultas de talento | Disponibilidad continua, sin intermediación |
| Equipo interno (admisiones/estudiantes/administrativo) | ~60% del tiempo repetitivo liberado para trabajo estratégico (análisis, retención, relación con el estudiante) | ~625 h/mes (modelo) |
| Institución | Imagen innovadora ante estudiantes y mercado; datos de consultas (intenciones, temas recurrentes, tickets) como insumo de decisión académica y de mercadeo | Activo de datos nuevo |

---

## 3. Métricas de éxito

| Métrica | Baseline | Meta | Fuente del dato |
|---|---|---|---|
| % de consultas resueltas sin humano | ~0% (todo cae al equipo) | ≥ 70% | Firestore `interactions`/`tickets` |
| Tiempo medio de respuesta (chatbot) | Horas-días (canal humano) | Segundos (< 30 s) | Cloud Logging / métricas Cloud Run |
| % de documentos auto-validados (✅ sin alertas) | 0% (100% manual) | 60–80% | Firestore `validations` |
| Tiempo por lote de 20 solicitudes | 2 h | ≤ 30 min | Medición de proceso en piloto |
| Satisfacción del usuario (CSAT) | Sin medición | ≥ 4.5 / 5 | Encuesta post-interacción |
| Costo por interacción | N/D (implícito en nómina) | Medirlo y reducirlo trimestralmente | Dashboard de costo GCP |

---

## 4. ROI aproximado (modelo simple)

### 4.1 Costo anual de la solución

| Componente | Supuesto | USD/año |
|---|---|---|
| Infraestructura GCP (MVP/piloto) | USD 80–350/mes → promedio ~USD 300/mes a volumen | ~3.600 |
| Equipo: 1.5 FTE | Ingeniero IA/fullstack USD 2.500/mes + 50% PM/analista USD 1.000/mes ≈ USD 3.500/mes (salarios Colombia, incluye prestaciones aproximadas) | ~42.000 |
| Otros (tests, capacitación, contingencia) | ~5% | ~2.300 |
| **Total año 1** | | **~USD 47.900** |

Nota de honestidad: el enunciado del caso fija el MVP en horas de una sesión; el 1.5 FTE modela el costo de sostener y escalar la solución en producción (Fases 1–3 del plan de implementación), que es el escenario relevante para ROI.

### 4.2 Ahorro anual valorizado

| Concepto | Cálculo | USD/año |
|---|---|---|
| Horas liberadas (run-rate) | ~625 h/mes × 12 | ~7.500 h |
| Valorización | × USD 7/h | **~52.500** |

Supuesto conservador adicional: solo el 70% de las horas liberadas se convierte en trabajo de valor (el resto se absorbe en curva de aprendizaje y variabilidad) → **ahorro efectivo ~USD 36.750/año**.

### 4.3 Resultado

| Escenario | Ahorro anual | Costo año 1 | Payback |
|---|---|---|---|
| Optimista (100% de horas capturadas) | USD 52.500 | USD 47.900 | ~11 meses |
| Base (70% de horas capturadas) | USD 36.750 | USD 47.900 | ~16 meses (año 2 positivo: costo recurrente cae a ~USD 45k sin implementación) |
| Conservador (50% de consultas: 150/día, 70% auto-resueltas) | ~USD 26.000 | USD 47.900 | ~22 meses |

**Lectura CFO:** el caso se sostiene por volumen. Si las 300 consultas/día se confirman en Fase 0, el payback está en ~11–16 meses y la capacidad recuperada (~3.5 FTE) puede reasignarse en lugar de contratar. Si el volumen real es la mitad, el proyecto sigue siendo positivo pero en año 2. La métrica decisiva a validar primero es el **volumen real de consultas/día**.

---

## 5. Beneficios no cuantificables (breve)

- **Velocidad de admisiones:** ciclo de admisión más corto puede mejorar tasas de conversión de inscritos (no modelado).
- **Calidad y trazabilidad:** cada interacción y validación queda registrada; hoy el proceso manual no genera datos analizables.
- **Escalabilidad sin contratar:** picos de demanda (matrículas, graduaciones) se absorben sin carga operativa adicional.
- **Cultura de datos:** decisiones de programas y mercadeo basadas en las intenciones reales de consulta.
- **Riesgo evitado:** reducción de errores humanos en validación documental y de inconsistencias en respuestas oficiales.

---

*Documento borrador. Modelo de estimación con supuestos declarados; no constituye auditoría financiera ni cotización.*
