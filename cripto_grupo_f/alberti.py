"""Simulador del Disco de Alberti con rotacion polialfabetica."""

from __future__ import annotations

from .texto import ALFABETO, normalizar


DISCO_INTERIOR = "phqgiumeaylnofdxjkrcvstzwb".upper()


def rotar_disco(posicion: int) -> str:
    posicion %= len(ALFABETO)
    return DISCO_INTERIOR[posicion:] + DISCO_INTERIOR[:posicion]


def posicion_desde_letra(letra: str) -> int:
    letra_normalizada = normalizar(letra, solo_letras=True)
    if not letra_normalizada:
        raise ValueError("La posicion debe contener una letra del alfabeto")
    return ALFABETO.index(letra_normalizada[0])


def cifrar(
    texto: str,
    posicion_inicial: int = 0,
    rotar_cada: int = 5,
    direccion: str = "derecha",
    avance: int = 1,
) -> dict[str, object]:
    return _procesar(texto, posicion_inicial, rotar_cada, modo="cifrar", direccion=direccion, avance=avance)


def descifrar(
    criptograma: str,
    posicion_inicial: int = 0,
    rotar_cada: int = 5,
    direccion: str = "derecha",
    avance: int = 1,
) -> dict[str, object]:
    return _procesar(criptograma, posicion_inicial, rotar_cada, modo="descifrar", direccion=direccion, avance=avance)


def _procesar(
    texto: str,
    posicion_inicial: int,
    rotar_cada: int,
    modo: str,
    direccion: str,
    avance: int,
) -> dict[str, object]:
    if rotar_cada <= 0:
        raise ValueError("rotar_cada debe ser mayor que cero")
    if avance <= 0:
        raise ValueError("avance debe ser mayor que cero")
    if direccion not in {"derecha", "izquierda"}:
        raise ValueError("direccion debe ser 'derecha' o 'izquierda'")

    texto_normalizado = normalizar(texto)
    resultado = []
    pasos = []
    letras_procesadas = 0
    posicion_actual = posicion_inicial % len(ALFABETO)

    for caracter in texto_normalizado:
        if caracter not in ALFABETO:
            resultado.append(caracter)
            pasos.append(
                {
                    "entrada": caracter,
                    "salida": caracter,
                    "posicion_disco": posicion_actual,
                    "alfabeto_interior": rotar_disco(posicion_actual),
                    "accion": "Se conserva porque no es letra",
                }
            )
            continue

        if letras_procesadas > 0 and letras_procesadas % rotar_cada == 0:
            if direccion == "derecha":
                posicion_actual = (posicion_actual + avance) % len(ALFABETO)
            else:
                posicion_actual = (posicion_actual - avance) % len(ALFABETO)

        alfabeto_interior = rotar_disco(posicion_actual)
        if modo == "cifrar":
            indice = ALFABETO.index(caracter)
            salida = alfabeto_interior[indice]
        elif modo == "descifrar":
            indice = alfabeto_interior.index(caracter)
            salida = ALFABETO[indice]
        else:
            raise ValueError("modo debe ser 'cifrar' o 'descifrar'")

        resultado.append(salida)
        letras_procesadas += 1
        pasos.append(
            {
                "entrada": caracter,
                "salida": salida,
                "posicion_disco": posicion_actual,
                "letra_indice": ALFABETO[posicion_actual],
                "alfabeto_exterior": ALFABETO,
                "alfabeto_interior": alfabeto_interior,
                "accion": f"{modo.capitalize()} con disco en posicion {posicion_actual} ({ALFABETO[posicion_actual]})",
            }
        )

    return {
        "modo": modo,
        "texto_entrada": texto_normalizado,
        "texto_salida": "".join(resultado),
        "posicion_inicial": posicion_inicial % len(ALFABETO),
        "letra_inicial": ALFABETO[posicion_inicial % len(ALFABETO)],
        "rotar_cada": rotar_cada,
        "direccion": direccion,
        "avance": avance,
        "pasos": pasos,
    }
