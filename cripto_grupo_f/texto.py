"""Utilidades de normalizacion de texto para los modulos criptograficos."""

from __future__ import annotations

import unicodedata


ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def quitar_acentos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(caracter for caracter in normalizado if unicodedata.category(caracter) != "Mn")


def normalizar(texto: str, solo_letras: bool = False) -> str:
    texto = quitar_acentos(texto).upper().replace("Ñ", "N")
    if solo_letras:
        return "".join(caracter for caracter in texto if caracter in ALFABETO)
    return texto
