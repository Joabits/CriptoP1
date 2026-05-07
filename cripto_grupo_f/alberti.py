"""Simulador del Disco de Alberti con rotacion polialfabetica."""

from __future__ import annotations

import unicodedata

from .texto import normalizar


# Alfabeto exterior historico de Alberti: letras latinas sin H, J, K, U, W, Y + numeros 1-4
ALFABETO_EXTERIOR = "ABCDEFGILMNOPQRSTVXZ1234"

# Alfabeto interior historico de Alberti: letras minusculas mezcladas + &, h, k, y
# El disco interior tiene 24 simbolos: letras en minuscula (sin j, u, w) + &, h, k, y
ALFABETO_INTERIOR = "&hkyabcdefgilmnopqrstvxz"

TIPO_DISCO_CLASICO = "clasico"
TIPO_DISCO_ESCOLAR = "escolar"


def _normalizar_texto(texto: str) -> str:
    """Convierte a mayusculas y elimina acentos."""
    texto = texto.upper()
    salida = []
    for caracter in texto:
        descomp = unicodedata.normalize("NFD", caracter)
        limpio = "".join(c for c in descomp if unicodedata.category(c) != "Mn")
        salida.append(limpio)
    return "".join(salida)


def rotar_disco(
    posicion: int,
    tipo_disco: str = TIPO_DISCO_CLASICO,
) -> str:
    """Rota el disco interior segun la posicion dada."""
    n = len(ALFABETO_INTERIOR)
    posicion %= n
    if tipo_disco == TIPO_DISCO_ESCOLAR:
        return ALFABETO_INTERIOR[posicion:] + ALFABETO_INTERIOR[:posicion]
    # Clasico: el simbolo en ALFABETO_INTERIOR en la posicion dada queda alineado con el primer simbolo exterior
    return ALFABETO_INTERIOR[posicion:] + ALFABETO_INTERIOR[:posicion]


def posicion_desde_letra(letra: str) -> int:
    """Devuelve el indice de una letra en el alfabeto interior."""
    letra = letra.lower()
    if letra not in ALFABETO_INTERIOR:
        raise ValueError(f"'{letra}' no pertenece al alfabeto interior")
    return ALFABETO_INTERIOR.index(letra)


def cifrar(
    texto: str,
    posicion_inicial: int = 0,
    rotar_cada: int = 5,
    direccion: str = "derecha",
    avance: int = 1,
    tipo_disco: str = TIPO_DISCO_CLASICO,
) -> dict[str, object]:
    return _procesar(
        texto, posicion_inicial, rotar_cada,
        modo="cifrar", direccion=direccion, avance=avance,
        tipo_disco=tipo_disco,
    )


def descifrar(
    criptograma: str,
    posicion_inicial: int = 0,
    rotar_cada: int = 5,
    direccion: str = "derecha",
    avance: int = 1,
    tipo_disco: str = TIPO_DISCO_CLASICO,
) -> dict[str, object]:
    return _procesar(
        criptograma, posicion_inicial, rotar_cada,
        modo="descifrar", direccion=direccion, avance=avance,
        tipo_disco=tipo_disco,
    )


def _procesar(
    texto: str,
    posicion_inicial: int,
    rotar_cada: int,
    modo: str,
    direccion: str,
    avance: int,
    tipo_disco: str,
) -> dict[str, object]:
    if rotar_cada <= 0:
        raise ValueError("rotar_cada debe ser mayor que cero")
    if avance <= 0:
        raise ValueError("avance debe ser mayor que cero")
    if direccion not in {"derecha", "izquierda"}:
        raise ValueError("direccion debe ser 'derecha' o 'izquierda'")

    n_ext = len(ALFABETO_EXTERIOR)
    n_int = len(ALFABETO_INTERIOR)
    assert n_ext == n_int, "Los alfabetos deben tener el mismo tamano"

    texto_normalizado = _normalizar_texto(texto)
    resultado = []
    pasos = []
    letras_procesadas = 0
    posicion_actual = posicion_inicial % n_int

    for caracter in texto_normalizado:
        if caracter not in ALFABETO_EXTERIOR:
            resultado.append(caracter)
            pasos.append({
                "entrada": caracter,
                "salida": caracter,
                "posicion_disco": posicion_actual,
                "alfabeto_interior": rotar_disco(posicion_actual, tipo_disco),
                "accion": "Se conserva porque no es letra del alfabeto exterior",
            })
            continue

        if letras_procesadas > 0 and letras_procesadas % rotar_cada == 0:
            if direccion == "derecha":
                posicion_actual = (posicion_actual + avance) % n_int
            else:
                posicion_actual = (posicion_actual - avance) % n_int

        alfabeto_interior_rotado = rotar_disco(posicion_actual, tipo_disco)

        if modo == "cifrar":
            indice = ALFABETO_EXTERIOR.index(caracter)
            salida = alfabeto_interior_rotado[indice]
        elif modo == "descifrar":
            if caracter not in alfabeto_interior_rotado:
                resultado.append(caracter)
                continue
            indice = alfabeto_interior_rotado.index(caracter)
            salida = ALFABETO_EXTERIOR[indice]
        else:
            raise ValueError("modo debe ser 'cifrar' o 'descifrar'")

        resultado.append(salida)
        letras_procesadas += 1
        pasos.append({
            "entrada": caracter,
            "salida": salida,
            "posicion_disco": posicion_actual,
            "simbolo_clave": ALFABETO_INTERIOR[posicion_actual],
            "alfabeto_exterior": ALFABETO_EXTERIOR,
            "alfabeto_interior": alfabeto_interior_rotado,
            "accion": f"{modo.capitalize()} '{caracter}' → '{salida}' con clave '{ALFABETO_INTERIOR[posicion_actual]}' (pos {posicion_actual})",
        })

    return {
        "modo": modo,
        "tipo_disco": tipo_disco,
        "texto_entrada": texto_normalizado,
        "texto_salida": "".join(resultado),
        "posicion_inicial": posicion_inicial % n_int,
        "simbolo_inicial": ALFABETO_INTERIOR[posicion_inicial % n_int],
        "rotar_cada": rotar_cada,
        "direccion": direccion,
        "avance": avance,
        "pasos": pasos,
    }