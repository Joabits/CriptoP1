"""Taller comparativo entre fuerza bruta y criptoanalisis tecnico."""

from __future__ import annotations

from .texto import ALFABETO, normalizar


PALABRAS_COMUNES = ["DE", "LA", "QUE", "EL", "EN", "Y", "A", "LOS", "DEL", "SE"]


def cifrar_cesar(texto: str, desplazamiento: int) -> str:
    desplazamiento %= len(ALFABETO)
    resultado = []
    for caracter in normalizar(texto):
        if caracter in ALFABETO:
            indice = ALFABETO.index(caracter)
            resultado.append(ALFABETO[(indice + desplazamiento) % len(ALFABETO)])
        else:
            resultado.append(caracter)
    return "".join(resultado)


def descifrar_cesar(texto: str, desplazamiento: int) -> str:
    return cifrar_cesar(texto, -desplazamiento)


def fuerza_bruta_cesar(criptograma: str) -> list[dict[str, object]]:
    candidatos = []
    for desplazamiento in range(1, len(ALFABETO)):
        texto = descifrar_cesar(criptograma, desplazamiento)
        candidatos.append(
            {
                "clave_probada": desplazamiento,
                "texto_posible": texto,
                "puntaje_linguistico": puntuar_espanol(texto),
            }
        )
    return sorted(candidatos, key=lambda item: item["puntaje_linguistico"], reverse=True)


def puntuar_espanol(texto: str) -> int:
    texto = f" {normalizar(texto)} "
    return sum(texto.count(f" {palabra} ") for palabra in PALABRAS_COMUNES)


def comparar_metodos() -> list[dict[str, str]]:
    return [
        {
            "aspecto": "Estrategia",
            "fuerza_bruta": "Prueba todas las claves posibles sin interpretar el sistema.",
            "criptoanalisis": "Estudia patrones, frecuencias y debilidades matematicas.",
        },
        {
            "aspecto": "Costo",
            "fuerza_bruta": "Crece con el tamano del espacio de claves.",
            "criptoanalisis": "Reduce el esfuerzo usando conocimiento del idioma o del algoritmo.",
        },
        {
            "aspecto": "Ejemplo",
            "fuerza_bruta": "Probar los 25 desplazamientos posibles de Cesar.",
            "criptoanalisis": "Detectar que la letra mas frecuente podria representar la E.",
        },
    ]
