"""Base de conocimiento institucional ESIC (datos SINTÉTICOS de demostración).

En producción esta KB viviría en Vertex AI Search con sincronización desde el CRM
y el sistema académico; para el MVP se versiona como dato curado en el repo y se
inyecta al prompt como grounding (mismo patrón, fuente distinta).
"""

PROGRAMAS = [
    {
        "id": "ESP-MKT-01",
        "nombre": "Especialización en Marketing Digital y Analítica",
        "modalidad": "Presencial (martes y jueves 6-9 pm) · 10 meses",
        "precio": "COP 18.500.000 (financiable hasta 12 cuotas)",
        "requisitos": "Título profesional, cédula, transcript universitario",
        "perfil": "Profesionales de marketing, administración o afines",
        "empleabilidad": "92% de egresados empleados a 6 meses · salario promedio +31% vs pregrado",
    },
    {
        "id": "ESP-DATA-02",
        "nombre": "Especialización en Ciencia de Datos y BI",
        "modalidad": "Híbrida (sábados) · 12 meses",
        "precio": "COP 21.000.000 (financiable hasta 18 cuotas)",
        "requisitos": "Título profesional, cédula, transcript, certificado laboral (1 año)",
        "perfil": "Ingenieros, economistas, administradores con base cuantitativa",
        "empleabilidad": "95% de egresados empleados a 6 meses · salario promedio +48% vs pregrado",
    },
    {
        "id": "ESP-FIN-03",
        "nombre": "Especialización en Finanzas y Gestión de Riesgo",
        "modalidad": "Presencial (lunes y miércoles 6-9 pm) · 10 meses",
        "precio": "COP 19.800.000 (financiable hasta 12 cuotas)",
        "requisitos": "Título profesional, cédula, transcript",
        "perfil": "Profesionales de finanzas, contaduría, economía",
        "empleabilidad": "90% de egresados empleados a 6 meses",
    },
    {
        "id": "MBA-04",
        "nombre": "MBA Internacional",
        "modalidad": "Híbrida · 16 meses · incluye semana internacional",
        "precio": "COP 45.000.000 (financiable hasta 24 cuotas)",
        "requisitos": "Título profesional, cédula, transcript, 3 años de experiencia",
        "perfil": "Profesionales con experiencia que buscan cargos de dirección",
        "empleabilidad": "89% de egresados ascendidos o cambiados de rol a 12 meses",
    },
]

FINANCIAMIENTO = [
    "Pago directo con 5% de descuento",
    "Financiación directa ESIC: hasta 24 cuotas sin intereses (según programa)",
    "Convenios con bancos (Bancolombia, Davivienda): crédito educativo a tasa preferencial",
    "Becas por mérito académico: 25%–50% del valor (convocatorias semestrales)",
    "Descuento egresados ESIC: 15%",
    "Financiación por empresa aliada (si el empleador tiene convenio marco)",
]

EMPLEO = [
    "Bolsa de empleo exclusiva para estudiantes y egresados ESIC",
    "Feria virtual de empleo 2 veces al año (60+ empresas aliadas)",
    "Programa de mentoría con egresados en cargos de dirección",
    "Prácticas y consultorías pagas para estudiantes de último módulo",
    "Convenios de doble certificación con empresas (Google, Microsoft, AWS)",
]

CONTACTO_HUMANO = {
    "admisiones": "admisiones.medellin@esic.demo · WhatsApp demo +57 604 000 0000",
    "financiero": "financiero.medellin@esic.demo · horario L-V 8am-6pm",
}
