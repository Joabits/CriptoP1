"""Analizador estadistico de monogramas para criptogramas en castellano."""

from __future__ import annotations

from collections import Counter

from .texto import ALFABETO, normalizar


FRECUENCIAS_CASTELLANO = {
    "E": 13.68,
    "A": 12.53,
    "O": 8.68,
    "S": 7.98,
    "R": 6.87,
    "N": 6.71,
    "I": 6.25,
    "D": 5.86,
    "C": 4.68,
    "L": 4.97,
    "T": 4.63,
    "U": 3.93,
    "M": 3.15,
    "P": 2.51,
    "B": 1.42,
    "G": 1.01,
    "V": 0.90,
    "Y": 0.90,
    "Q": 0.88,
    "H": 0.70,
    "F": 0.69,
    "Z": 0.52,
    "J": 0.44,
    "X": 0.22,
    "K": 0.02,
    "W": 0.01,
}

LETRAS_ESTIRANDO = ["E", "A", "O", "S", "R", "N", "I", "D", "C"]
DIGRAMAS_COMUNES = ["DE", "EN", "ES", "LA", "EL", "OS", "AS", "AR", "ER", "RA"]
TRIGRAMAS_COMUNES = ["QUE", "LOS", "DEL", "LAS", "CON", "EST", "ENT", "ION", "PAR", "ARA"]


def contar_monogramas(texto: str) -> Counter[str]:
    letras = normalizar(texto, solo_letras=True)
    return Counter(letras)


def calcular_frecuencias(texto: str) -> list[dict[str, object]]:
    conteos = contar_monogramas(texto)
    total = sum(conteos.values())
    if total == 0:
        return []

    filas = []
    for letra, cantidad in conteos.most_common():
        filas.append(
            {
                "letra": letra,
                "conteo": cantidad,
                "frecuencia_%": round((cantidad / total) * 100, 2),
                "castellano_%": FRECUENCIAS_CASTELLANO.get(letra, 0),
            }
        )
    return filas


def sugerir_sustituciones(texto: str, limite: int = 9) -> list[dict[str, str | int]]:
    conteos = contar_monogramas(texto)
    letras_criptograma = [letra for letra, _ in conteos.most_common(limite)]
    sugeridas = LETRAS_ESTIRANDO[: len(letras_criptograma)]
    return [
        {
            "letra_cifrada": cifrada,
            "sugerencia_texto_plano": plana,
            "posicion_frecuencia": indice + 1,
        }
        for indice, (cifrada, plana) in enumerate(zip(letras_criptograma, sugeridas))
    ]


def aplicar_sustituciones(texto: str, sustituciones: dict[str, str]) -> str:
    resultado = []
    for caracter in normalizar(texto):
        if caracter in ALFABETO:
            resultado.append(sustituciones.get(caracter, "_"))
        else:
            resultado.append(caracter)
    return "".join(resultado)


def contar_ngramas(texto: str, longitud: int = 2, limite: int = 10) -> list[dict[str, object]]:
    if longitud <= 0:
        raise ValueError("longitud debe ser mayor que cero")

    letras = normalizar(texto, solo_letras=True)
    if len(letras) < longitud:
        return []

    ngramas = Counter(letras[indice : indice + longitud] for indice in range(len(letras) - longitud + 1))
    total = sum(ngramas.values())
    return [
        {
            "ngrama": ngrama,
            "conteo": cantidad,
            "frecuencia_%": round((cantidad / total) * 100, 2),
        }
        for ngrama, cantidad in ngramas.most_common(limite)
    ]


def coincidencias_ngramas(texto: str, longitud: int = 2) -> list[dict[str, object]]:
    comunes = DIGRAMAS_COMUNES if longitud == 2 else TRIGRAMAS_COMUNES
    observados = {item["ngrama"]: item for item in contar_ngramas(texto, longitud, limite=50)}
    return [
        {
            "patron_castellano": patron,
            "aparece_en_criptograma": patron in observados,
            "conteo": observados.get(patron, {}).get("conteo", 0),
        }
        for patron in comunes
    ]


def parsear_sustituciones(texto_mapa: str) -> dict[str, str]:
    sustituciones = {}
    partes = texto_mapa.replace("\n", ",").replace(";", ",").split(",")
    for parte in partes:
        if not parte.strip():
            continue
        if "=" in parte:
            origen, destino = parte.split("=", 1)
        elif "->" in parte:
            origen, destino = parte.split("->", 1)
        elif ":" in parte:
            origen, destino = parte.split(":", 1)
        else:
            raise ValueError(f"Formato invalido: {parte.strip()}")

        origen = normalizar(origen, solo_letras=True)
        destino = normalizar(destino, solo_letras=True)
        if len(origen) != 1 or len(destino) != 1:
            raise ValueError("Cada sustitucion debe usar una letra cifrada y una letra plana")
        sustituciones[origen] = destino
    return sustituciones


def porcentaje_estirando(texto: str) -> float:
    conteos = contar_monogramas(texto)
    total = sum(conteos.values())
    if total == 0:
        return 0.0
    apariciones = sum(conteos[letra] for letra in LETRAS_ESTIRANDO)
    return round((apariciones / total) * 100, 2)
