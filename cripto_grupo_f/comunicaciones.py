"""Comparacion entre sistemas aislados e interconectados."""

from __future__ import annotations


COMPARATIVA = [
    {
        "criterio": "Superficie de ataque",
        "sistema_aislado": "Baja: pocos puntos de entrada externos",
        "sistema_interconectado": "Alta: red, usuarios, servidores, APIs y canales",
    },
    {
        "criterio": "Confidencialidad",
        "sistema_aislado": "Depende principalmente del acceso fisico",
        "sistema_interconectado": "Depende del cifrado, autenticacion y gestion de claves",
    },
    {
        "criterio": "Integridad",
        "sistema_aislado": "Cambios limitados a usuarios locales",
        "sistema_interconectado": "Riesgo de alteracion durante la transmision",
    },
    {
        "criterio": "Disponibilidad",
        "sistema_aislado": "Menos dependencia de la red",
        "sistema_interconectado": "Expuesto a fallas de red, DoS y servicios externos",
    },
]


def obtener_comparativa() -> list[dict[str, str]]:
    return COMPARATIVA.copy()


def evaluar_canal(cifrado: bool, autenticado: bool, integridad: bool) -> dict[str, object]:
    puntaje = sum([cifrado, autenticado, integridad])
    if puntaje == 3:
        estado = "Canal seguro"
        riesgo = "Bajo"
    elif puntaje == 2:
        estado = "Canal parcialmente seguro"
        riesgo = "Medio"
    else:
        estado = "Canal inseguro"
        riesgo = "Alto"

    faltantes = []
    if not cifrado:
        faltantes.append("confidencialidad mediante cifrado")
    if not autenticado:
        faltantes.append("autenticacion del emisor y receptor")
    if not integridad:
        faltantes.append("verificacion de integridad del mensaje")

    return {
        "puntaje": puntaje,
        "estado": estado,
        "riesgo": riesgo,
        "faltantes": faltantes,
    }


def simular_transmision(mensaje: str, atacante_intercepta: bool, canal_cifrado: bool) -> dict[str, str]:
    if not atacante_intercepta:
        observado = "El atacante no logra observar el canal."
    elif canal_cifrado:
        observado = "El atacante ve datos cifrados, no el contenido legible."
    else:
        observado = f"El atacante puede leer el mensaje: {mensaje}"

    return {
        "mensaje_original": mensaje,
        "canal": "Cifrado" if canal_cifrado else "Sin cifrar",
        "observacion_del_atacante": observado,
    }
