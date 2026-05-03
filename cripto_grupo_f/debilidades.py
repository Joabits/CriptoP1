"""Mapeo de activos, debilidades, amenazas y controles."""

from __future__ import annotations


MAPA_DEBILIDADES = {
    "Hardware": [
        {
            "activo": "Computadoras y laptops",
            "vulnerabilidad": "Falta de control fisico y etiquetado",
            "tipo_amenaza": "Intercepcion o robo fisico",
            "amenaza": "Robo o manipulacion no autorizada",
            "impacto": "Perdida de disponibilidad y posible fuga de datos",
            "control": "Inventario, candados, control de acceso y cifrado de disco",
        },
        {
            "activo": "Servidores",
            "vulnerabilidad": "Ubicacion sin proteccion ambiental",
            "tipo_amenaza": "Interrupcion del servicio",
            "amenaza": "Dano fisico, fallas electricas o sabotaje",
            "impacto": "Interrupcion de servicios criticos",
            "control": "UPS, sala segura, monitoreo y respaldo de energia",
        },
    ],
    "Software": [
        {
            "activo": "Sistema operativo",
            "vulnerabilidad": "Parches de seguridad pendientes",
            "tipo_amenaza": "Explotacion tecnica",
            "amenaza": "Explotacion de vulnerabilidades conocidas",
            "impacto": "Ejecucion de malware o acceso no autorizado",
            "control": "Gestion de actualizaciones y escaneo periodico",
        },
        {
            "activo": "Aplicaciones academicas",
            "vulnerabilidad": "Autenticacion debil",
            "tipo_amenaza": "Suplantacion",
            "amenaza": "Suplantacion de identidad",
            "impacto": "Modificacion o consulta indebida de expedientes",
            "control": "MFA, politicas de contrasena y bloqueo por intentos",
        },
    ],
    "Datos": [
        {
            "activo": "Expedientes academicos",
            "vulnerabilidad": "Datos almacenados sin cifrado",
            "tipo_amenaza": "Divulgacion de informacion",
            "amenaza": "Divulgacion de informacion confidencial",
            "impacto": "Perdida de confidencialidad y sanciones institucionales",
            "control": "Cifrado, control de permisos y registro de accesos",
        },
        {
            "activo": "Copias de seguridad",
            "vulnerabilidad": "Respaldos sin validacion ni proteccion",
            "tipo_amenaza": "Perdida o alteracion de datos",
            "amenaza": "Perdida, corrupcion o secuestro de datos",
            "impacto": "Imposibilidad de recuperacion ante incidentes",
            "control": "Regla 3-2-1, pruebas de restauracion y almacenamiento seguro",
        },
    ],
}


def tipos_de_activo() -> list[str]:
    return list(MAPA_DEBILIDADES.keys())


def obtener_debilidades(tipo_activo: str | None = None) -> list[dict[str, str]]:
    if tipo_activo is None or tipo_activo == "Todos":
        return [item for lista in MAPA_DEBILIDADES.values() for item in lista]
    return MAPA_DEBILIDADES.get(tipo_activo, [])


def resumen_por_tipo() -> list[dict[str, str | int]]:
    return [
        {"tipo": tipo, "activos_analizados": len(items)}
        for tipo, items in MAPA_DEBILIDADES.items()
    ]


def controles_recomendados(tipo_activo: str) -> list[str]:
    return [item["control"] for item in obtener_debilidades(tipo_activo)]
