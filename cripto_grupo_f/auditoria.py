"""Simulador de auditoria academica con preguntas de control."""

from __future__ import annotations


PREGUNTAS_CONTROL = {
    "P1": {
        "pregunta": "Los expedientes academicos estan cifrados en reposo?",
        "principio": "Confidencialidad",
        "recomendacion": "Aplicar cifrado a la base de datos y a respaldos.",
    },
    "P2": {
        "pregunta": "Solo usuarios autorizados pueden consultar o modificar expedientes?",
        "principio": "Control de acceso",
        "recomendacion": "Usar roles, MFA y permisos de minimo privilegio.",
    },
    "P3": {
        "pregunta": "Existe registro de accesos y cambios sobre cada expediente?",
        "principio": "Trazabilidad e integridad",
        "recomendacion": "Registrar auditoria con fecha, usuario, accion y origen.",
    },
    "P4": {
        "pregunta": "Hay copias de seguridad verificadas y protegidas?",
        "principio": "Disponibilidad",
        "recomendacion": "Probar restauraciones y proteger respaldos contra alteracion.",
    },
}


def obtener_preguntas() -> dict[str, dict[str, str]]:
    return PREGUNTAS_CONTROL.copy()


def evaluar_auditoria(respuestas: dict[str, bool]) -> dict[str, object]:
    cumplidas = [codigo for codigo, valor in respuestas.items() if valor]
    incumplidas = [codigo for codigo in PREGUNTAS_CONTROL if not respuestas.get(codigo, False)]
    puntaje = len(cumplidas)

    if puntaje == 4:
        estado = "Seguro"
        nivel = "Bajo riesgo"
    elif puntaje >= 2:
        estado = "Parcialmente seguro"
        nivel = "Riesgo medio"
    else:
        estado = "Inseguro"
        nivel = "Riesgo alto"

    recomendaciones = [PREGUNTAS_CONTROL[codigo]["recomendacion"] for codigo in incumplidas]
    return {
        "puntaje": puntaje,
        "maximo": len(PREGUNTAS_CONTROL),
        "estado": estado,
        "nivel": nivel,
        "cumplidas": cumplidas,
        "incumplidas": incumplidas,
        "recomendaciones": recomendaciones,
    }
