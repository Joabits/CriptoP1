"""Simulador del Disco de Alberti con rotacion polialfabetica."""

from __future__ import annotations

import random
import unicodedata

from .texto import ALFABETO as _ALFABETO_DEFECTO, normalizar


ALFABETO = _ALFABETO_DEFECTO
ALFABETO_ES = "ABCDEFGHIJKLMN" + "\u00d1" + "OPQRSTUVWXYZ"
DISCO_INTERIOR = "phqgiumeaylnofdxjkrcvstzwb".upper()
TIPO_DISCO_CLASICO = "clasico"
TIPO_DISCO_ESCOLAR = "escolar"


def _disco_interior_para(alfabeto: str, tipo_disco: str = TIPO_DISCO_CLASICO) -> str:
    if tipo_disco == TIPO_DISCO_ESCOLAR:
        return alfabeto
    if alfabeto == _ALFABETO_DEFECTO:
        return DISCO_INTERIOR
    rng = random.Random(42)
    letras = list(alfabeto)
    rng.shuffle(letras)
    return "".join(letras)


def _normalizar_para(texto: str, alfabeto: str) -> str:
    texto = texto.upper()
    if "\u00d1" in alfabeto:
        salida = []
        for caracter in texto:
            if caracter == "\u00d1":
                salida.append(caracter)
                continue
            descomp = unicodedata.normalize("NFD", caracter)
            limpio = "".join(c for c in descomp if unicodedata.category(c) != "Mn")
            salida.append(limpio)
        return "".join(salida)
    return normalizar(texto)


def rotar_disco(
    posicion: int,
    alfabeto: str | None = None,
    tipo_disco: str = TIPO_DISCO_CLASICO,
) -> str:
    alfabeto = alfabeto or ALFABETO
    disco = _disco_interior_para(alfabeto, tipo_disco)
    posicion %= len(alfabeto)
    letra_clave = alfabeto[posicion]
    indice_clave = disco.index(letra_clave)
    return disco[indice_clave:] + disco[:indice_clave]


def posicion_desde_letra(letra: str, alfabeto: str | None = None) -> int:
    alfabeto = alfabeto or ALFABETO
    letra_normalizada = _normalizar_para(letra, alfabeto)
    letra_normalizada = "".join(c for c in letra_normalizada if c in alfabeto)
    if not letra_normalizada:
        raise ValueError("La posicion debe contener una letra del alfabeto")
    return alfabeto.index(letra_normalizada[0])


def cifrar(
    texto: str,
    posicion_inicial: int = 0,
    rotar_cada: int = 5,
    direccion: str = "derecha",
    avance: int = 1,
    alfabeto: str | None = None,
    tipo_disco: str = TIPO_DISCO_CLASICO,
) -> dict[str, object]:
    return _procesar(
        texto, posicion_inicial, rotar_cada,
        modo="cifrar", direccion=direccion, avance=avance,
        alfabeto=alfabeto or ALFABETO, tipo_disco=tipo_disco,
    )


def descifrar(
    criptograma: str,
    posicion_inicial: int = 0,
    rotar_cada: int = 5,
    direccion: str = "derecha",
    avance: int = 1,
    alfabeto: str | None = None,
    tipo_disco: str = TIPO_DISCO_CLASICO,
) -> dict[str, object]:
    return _procesar(
        criptograma, posicion_inicial, rotar_cada,
        modo="descifrar", direccion=direccion, avance=avance,
        alfabeto=alfabeto or ALFABETO, tipo_disco=tipo_disco,
    )


def _procesar(
    texto: str,
    posicion_inicial: int,
    rotar_cada: int,
    modo: str,
    direccion: str,
    avance: int,
    alfabeto: str,
    tipo_disco: str,
) -> dict[str, object]:
    if rotar_cada <= 0:
        raise ValueError("rotar_cada debe ser mayor que cero")
    if avance <= 0:
        raise ValueError("avance debe ser mayor que cero")
    if direccion not in {"derecha", "izquierda"}:
        raise ValueError("direccion debe ser 'derecha' o 'izquierda'")

    texto_normalizado = _normalizar_para(texto, alfabeto)
    resultado = []
    pasos = []
    letras_procesadas = 0
    posicion_actual = posicion_inicial % len(alfabeto)

    for caracter in texto_normalizado:
        if caracter not in alfabeto:
            resultado.append(caracter)
            pasos.append(
                {
                    "entrada": caracter,
                    "salida": caracter,
                    "posicion_disco": posicion_actual,
                    "alfabeto_interior": rotar_disco(posicion_actual, alfabeto, tipo_disco),
                    "accion": "Se conserva porque no es letra",
                }
            )
            continue

        if letras_procesadas > 0 and letras_procesadas % rotar_cada == 0:
            if direccion == "derecha":
                posicion_actual = (posicion_actual + avance) % len(alfabeto)
            else:
                posicion_actual = (posicion_actual - avance) % len(alfabeto)

        alfabeto_interior = rotar_disco(posicion_actual, alfabeto, tipo_disco)
        if modo == "cifrar":
            indice = alfabeto.index(caracter)
            salida = alfabeto_interior[indice]
        elif modo == "descifrar":
            indice = alfabeto_interior.index(caracter)
            salida = alfabeto[indice]
        else:
            raise ValueError("modo debe ser 'cifrar' o 'descifrar'")

        resultado.append(salida)
        letras_procesadas += 1
        pasos.append(
            {
                "entrada": caracter,
                "salida": salida,
                "posicion_disco": posicion_actual,
                "letra_clave": alfabeto[posicion_actual],
                "alfabeto_exterior": alfabeto,
                "alfabeto_interior": alfabeto_interior,
                "accion": f"{modo.capitalize()} con clave {alfabeto[posicion_actual]} en posicion {posicion_actual}",
            }
        )

    return {
        "modo": modo,
        "alfabeto": alfabeto,
        "tipo_disco": tipo_disco,
        "texto_entrada": texto_normalizado,
        "texto_salida": "".join(resultado),
        "posicion_inicial": posicion_inicial % len(alfabeto),
        "letra_inicial": alfabeto[posicion_inicial % len(alfabeto)],
        "rotar_cada": rotar_cada,
        "direccion": direccion,
        "avance": avance,
        "pasos": pasos,
    }
