"""Taller comparativo entre fuerza bruta y criptoanalisis tecnico."""

from __future__ import annotations

from collections import Counter

from .texto import ALFABETO, quitar_acentos, normalizar


ALFABETO_INGLES = ALFABETO
ALFABETO_ESPANOL = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
ALFABETOS_CESAR = {
    "Ingles": ALFABETO_INGLES,
    "Espanol": ALFABETO_ESPANOL,
}


PALABRAS_COMUNES = [
    "DE",
    "LA",
    "QUE",
    "EL",
    "EN",
    "Y",
    "A",
    "LOS",
    "DEL",
    "SE",
    "HOLA",
    "ESTE",
    "TEXTO",
    "PARA",
    "UNA",
    "PISTA",
    "TECNICA",
    "CRIPTOGRAFIA",
    "INFORMACION",
    "SEGURIDAD",
    "CANAL",
]


def definiciones_autores() -> list[dict[str, str]]:
    return [
        {
            "autor": "Kerckhoffs",
            "idea": "La seguridad no debe depender de ocultar el algoritmo, sino de proteger la clave.",
            "aporte_al_taller": "Permite analizar publicamente el metodo Cesar y concentrar la evaluacion en la clave.",
        },
        {
            "autor": "Shannon",
            "idea": "La seguridad se estudia por la estructura del sistema y por la informacion que revela el criptograma.",
            "aporte_al_taller": "Ayuda a distinguir un intento ciego de un analisis tecnico de patrones y redundancia.",
        },
        {
            "autor": "Menezes, van Oorschot y Vanstone",
            "idea": "El criptoanalisis busca recuperar texto plano, clave o informacion util sin conocer la clave secreta.",
            "aporte_al_taller": "Define el ataque como un estudio sistematico del criptosistema, no solo como adivinacion.",
        },
        {
            "autor": "Stallings / Paar y Pelzl",
            "idea": "La busqueda exhaustiva prueba claves posibles; su costo depende del tamano del espacio de claves.",
            "aporte_al_taller": "Ubica la fuerza bruta como metodo burdo cuando no usa propiedades del idioma ni del algoritmo.",
        },
    ]


def normalizar_para_cesar(texto: str, alfabeto: str = ALFABETO_INGLES, solo_letras: bool = False) -> str:
    if "Ñ" not in alfabeto:
        return normalizar(texto, solo_letras=solo_letras)

    marcador = "__ENIE__"
    texto_normalizado = quitar_acentos(texto.upper().replace("Ñ", marcador)).replace(marcador, "Ñ")
    if solo_letras:
        return "".join(caracter for caracter in texto_normalizado if caracter in alfabeto)
    return texto_normalizado


def cifrar_cesar(texto: str, desplazamiento: int, alfabeto: str = ALFABETO_INGLES) -> str:
    desplazamiento %= len(alfabeto)
    resultado = []
    for caracter in normalizar_para_cesar(texto, alfabeto):
        if caracter in alfabeto:
            indice = alfabeto.index(caracter)
            resultado.append(alfabeto[(indice + desplazamiento) % len(alfabeto)])
        else:
            resultado.append(caracter)
    return "".join(resultado)


def descifrar_cesar(texto: str, desplazamiento: int, alfabeto: str = ALFABETO_INGLES) -> str:
    return cifrar_cesar(texto, -desplazamiento, alfabeto)


def fuerza_bruta_cesar(criptograma: str, alfabeto: str = ALFABETO_INGLES) -> list[dict[str, object]]:
    candidatos = []
    for desplazamiento in range(1, len(alfabeto)):
        texto = descifrar_cesar(criptograma, desplazamiento, alfabeto)
        candidatos.append(
            {
                "clave_probada": desplazamiento,
                "texto_posible": texto,
                "puntaje_linguistico": puntuar_espanol(texto),
            }
        )
    return sorted(candidatos, key=lambda item: item["puntaje_linguistico"], reverse=True)


def analisis_criptoanalitico_cesar(
    criptograma: str, alfabeto: str = ALFABETO_INGLES
) -> list[dict[str, object]]:
    letras = normalizar_para_cesar(criptograma, alfabeto, solo_letras=True)
    if not letras:
        return []

    frecuencias = dict(Counter(letras).most_common(5))
    candidatos = []
    for clave_sugerida in range(1, len(alfabeto)):
        texto_posible = descifrar_cesar(criptograma, clave_sugerida, alfabeto)
        letra_esperada = alfabeto[(alfabeto.index("E") + clave_sugerida) % len(alfabeto)]
        conteo = frecuencias.get(letra_esperada, 0)
        candidatos.append(
            {
                "indicio": f"{letra_esperada} aparece {conteo} veces",
                "hipotesis": f"con clave {clave_sugerida}, {letra_esperada} representaria E",
                "clave_sugerida": clave_sugerida,
                "texto_posible": texto_posible,
                "coincidencias_frecuencia": conteo,
                "puntaje_linguistico": puntuar_espanol(texto_posible),
            }
        )
    return sorted(
        candidatos,
        key=lambda item: (item["puntaje_linguistico"], item["coincidencias_frecuencia"]),
        reverse=True,
    )


def puntuar_espanol(texto: str) -> int:
    texto = f" {normalizar(texto)} "
    return sum(texto.count(f" {palabra} ") for palabra in PALABRAS_COMUNES)


def comparar_metodos() -> list[dict[str, str]]:
    return [
        {
            "aspecto": "Estrategia",
            "fuerza_bruta": "Prueba todas las claves posibles sin interpretar el sistema: es exhaustiva y burda.",
            "criptoanalisis": "Estudia el algoritmo, el idioma, frecuencias y debilidades matematicas.",
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
        {
            "aspecto": "Resultado esperado",
            "fuerza_bruta": "Entrega una lista de candidatos y exige revisar cual parece legible.",
            "criptoanalisis": "Formula hipotesis, prioriza claves probables y justifica la eleccion.",
        },
    ]
